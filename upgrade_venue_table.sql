-- 升级venues表结构 - 添加生产级别字段
-- 执行前请备份数据库！

USE exam_system; -- 请根据实际数据库名修改

-- 添加新字段
ALTER TABLE venues 
ADD COLUMN address VARCHAR(255) COMMENT '考场地址',
ADD COLUMN description TEXT COMMENT '考场描述',
ADD COLUMN capacity INT NOT NULL DEFAULT 0 COMMENT '容纳人数',
ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否激活',
ADD COLUMN contact_person VARCHAR(50) COMMENT '联系人',
ADD COLUMN contact_phone VARCHAR(20) COMMENT '联系电话',
ADD COLUMN equipment_info TEXT COMMENT '设备信息';

-- 修改status字段类型（如果需要）
ALTER TABLE venues MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT '状态(active/inactive)';

-- 创建索引提升查询性能
CREATE INDEX idx_venues_status ON venues(status);
CREATE INDEX idx_venues_type ON venues(type);
CREATE INDEX idx_venues_is_active ON venues(is_active);
CREATE INDEX idx_venues_name ON venues(name);

-- 验证表结构
DESCRIBE venues;

-- 显示升级后的统计信息
SELECT 
    COUNT(*) as total_venues,
    SUM(CASE WHEN is_active = 1 AND status = 'active' THEN 1 ELSE 0 END) as active_venues,
    SUM(capacity) as total_capacity,
    AVG(capacity) as avg_capacity,
    COUNT(DISTINCT type) as venue_types
FROM venues;