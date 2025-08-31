# 修复后的手动签到路由实现

@router.post("/manual-checkin/query", response_model=ManualCheckinQueryResponse, summary="查询考生信息用于手动签到")
async def query_candidate_for_manual_checkin(
    query_data: ManualCheckinQueryRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """第一步：根据考生姓名和身份证查询考试信息"""
    # 检查权限：只有考务人员可以进行手动签到查询
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考务人员可以进行手动签到操作"
        )
    
    # 使用正确的服务类
    service = ManualCheckinService(db)
    try:
        result = service.query_candidate_for_manual_checkin(
            real_name=query_data.real_name,
            id_card=query_data.id_card
        )
        return ManualCheckinQueryResponse(**result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询考生信息失败: {str(e)}"
        )


@router.post("/manual-checkin/confirm", response_model=ManualCheckinConfirmResponse, summary="确认手动签到")
async def confirm_manual_checkin(
    confirm_data: ManualCheckinConfirmRequest,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """第二步：确认执行手动签到"""
    # 检查权限：只有考务人员可以进行手动签到确认
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.EXAMINER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有考务人员可以进行手动签到操作"
        )
    
    # 使用正确的服务类
    service = ManualCheckinService(db)
    try:
        # 构建操作员信息
        operator_info = confirm_data.operator_info or f"工作人员({current_user.real_name or current_user.username})"
        
        result = service.confirm_manual_checkin(
            candidate_id=confirm_data.candidate_id,
            schedule_id=confirm_data.schedule_id,
            operator_info=operator_info
        )
        
        # 检查业务逻辑返回的结果
        if not result.get("success", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message", "签到失败")
            )
            
        return ManualCheckinConfirmResponse(**result)
    except HTTPException:
        raise  # 重新抛出HTTP异常
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"签到操作失败: {str(e)}"
        )