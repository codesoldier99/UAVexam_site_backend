<template>
  <div class="assignment-manager page-container">
    <div class="page-header">
      <h2 class="page-title">人员分配管理</h2>
      <p class="page-description">管理考试的考官和考生分配</p>
    </div>
    
    <!-- 选择考试 -->
    <el-card class="select-exam-card">
      <div class="select-exam-container">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="考试名称">
            <el-input v-model="searchForm.name" placeholder="请输入考试名称" clearable />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="未开始" value="pending" />
              <el-option label="进行中" value="ongoing" />
              <el-option label="已结束" value="completed" />
              <el-option label="已取消" value="cancelled" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
            <el-button @click="resetSearch">
              <el-icon><Refresh /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 考试列表 -->
      <el-table
        v-loading="loading"
        :data="examList"
        border
        style="width: 100%"
        @row-click="handleSelectExam"
        highlight-current-row
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="考试名称" min-width="200" />
        <el-table-column prop="exam_type" label="考试类型" width="120" />
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="考官数" width="100" align="center">
          <template #default="scope">
            {{ scope.row.examiners_count || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="考生数" width="100" align="center">
          <template #default="scope">
            {{ scope.row.candidates_count || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click.stop="handleManage(scope.row)">
              人员管理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 人员分配管理 -->
    <div v-if="selectedExam" class="assignment-container">
      <el-card class="exam-info-card">
        <template #header>
          <div class="card-header">
            <span>考试信息</span>
          </div>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="考试名称">{{ selectedExam.name }}</el-descriptions-item>
          <el-descriptions-item label="考试类型">{{ selectedExam.exam_type }}</el-descriptions-item>
          <el-descriptions-item label="开始日期">{{ selectedExam.start_date }}</el-descriptions-item>
          <el-descriptions-item label="结束日期">{{ selectedExam.end_date }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(selectedExam.status)">
              {{ getStatusText(selectedExam.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedExam.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </el-card>
      
      <!-- 考官分配 -->
      <el-card class="examiners-card">
        <template #header>
          <div class="card-header">
            <span>考官分配</span>
            <el-button type="primary" size="small" @click="handleAssignExaminers">
              <el-icon><Plus /></el-icon>
              分配考官
            </el-button>
          </div>
        </template>
        <el-table
          v-loading="examinersLoading"
          :data="assignedExaminers"
          border
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="gender" label="性别" width="80">
            <template #default="scope">
              {{ scope.row.gender === 'male' ? '男' : '女' }}
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="联系电话" width="150" />
          <el-table-column prop="email" label="电子邮箱" min-width="180" />
          <el-table-column prop="certificate_no" label="证书编号" width="150" />
          <el-table-column prop="qualification" label="资质等级" width="120">
            <template #default="scope">
              {{ getQualificationText(scope.row.qualification) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-popconfirm
                title="确定要移除此考官吗？"
                @confirm="handleRemoveExaminer(scope.row)"
              >
                <template #reference>
                  <el-button link type="danger">移除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="assignedExaminers.length === 0" class="empty-data">
          <el-empty description="暂无分配的考官" />
        </div>
      </el-card>
      
      <!-- 考生分配 -->
      <el-card class="candidates-card">
        <template #header>
          <div class="card-header">
            <span>考生分配</span>
            <div class="header-actions">
              <el-button type="primary" size="small" @click="handleAssignCandidates">
                <el-icon><Plus /></el-icon>
                分配考生
              </el-button>
              <el-button type="success" size="small" @click="handleBatchAssign">
                <el-icon><Upload /></el-icon>
                批量导入
              </el-button>
            </div>
          </div>
        </template>
        <div class="candidates-search">
          <el-input
            v-model="candidateSearchKeyword"
            placeholder="搜索考生姓名、身份证号"
            clearable
            @input="handleCandidateSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        <el-table
          v-loading="candidatesLoading"
          :data="assignedCandidates"
          border
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="gender" label="性别" width="80">
            <template #default="scope">
              {{ scope.row.gender === 'male' ? '男' : '女' }}
            </template>
          </el-table-column>
          <el-table-column prop="id_card" label="身份证号" width="180" />
          <el-table-column prop="phone" label="联系电话" width="150" />
          <el-table-column prop="organization" label="所属单位" min-width="150" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-popconfirm
                title="确定要移除此考生吗？"
                @confirm="handleRemoveCandidate(scope.row)"
              >
                <template #reference>
                  <el-button link type="danger">移除</el-button>
                </template>
              </el-popconfirm>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="assignedCandidates.length === 0" class="empty-data">
          <el-empty description="暂无分配的考生" />
        </div>
        
        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="candidatesCurrentPage"
            v-model:page-size="candidatesPageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="candidatesTotal"
            @size-change="handleCandidatesSizeChange"
            @current-change="handleCandidatesCurrentChange"
          />
        </div>
      </el-card>
    </div>
    
    <!-- 分配考官对话框 -->
    <el-dialog
      v-model="assignExaminersVisible"
      title="分配考官"
      width="800px"
    >
      <div class="assign-examiners-container">
        <div class="search-container">
          <el-input
            v-model="examinerSearchKeyword"
            placeholder="搜索考官姓名、证书编号"
            clearable
            @input="handleExaminerSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        
        <el-table
          v-loading="availableExaminersLoading"
          :data="availableExaminers"
          border
          style="width: 100%"
          @selection-change="handleExaminerSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="gender" label="性别" width="80">
            <template #default="scope">
              {{ scope.row.gender === 'male' ? '男' : '女' }}
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="联系电话" width="150" />
          <el-table-column prop="certificate_no" label="证书编号" width="150" />
          <el-table-column prop="qualification" label="资质等级" width="120">
            <template #default="scope">
              {{ getQualificationText(scope.row.qualification) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">
                {{ scope.row.status === 'active' ? '在职' : '离职' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="examinersSearchPage"
            v-model:page-size="examinersSearchPageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="examinersSearchTotal"
            @size-change="handleExaminersSearchSizeChange"
            @current-change="handleExaminersSearchCurrentChange"
          />
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="assignExaminersVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAssignExaminers" :loading="assignExaminersLoading">
            确认分配
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 分配考生对话框 -->
    <el-dialog
      v-model="assignCandidatesVisible"
      title="分配考生"
      width="800px"
    >
      <div class="assign-candidates-container">
        <div class="search-container">
          <el-form :inline="true" :model="candidatesSearchForm" class="search-form">
            <el-form-item label="姓名">
              <el-input v-model="candidatesSearchForm.name" placeholder="请输入考生姓名" clearable />
            </el-form-item>
            <el-form-item label="身份证号">
              <el-input v-model="candidatesSearchForm.id_card" placeholder="请输入身份证号" clearable />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleCandidatesSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
              <el-button @click="resetCandidatesSearch">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </div>
        
        <el-table
          v-loading="availableCandidatesLoading"
          :data="availableCandidates"
          border
          style="width: 100%"
          @selection-change="handleCandidateSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="name" label="姓名" width="120" />
          <el-table-column prop="gender" label="性别" width="80">
            <template #default="scope">
              {{ scope.row.gender === 'male' ? '男' : '女' }}
            </template>
          </el-table-column>
          <el-table-column prop="id_card" label="身份证号" width="180" />
          <el-table-column prop="phone" label="联系电话" width="150" />
          <el-table-column prop="organization" label="所属单位" min-width="150" />
        </el-table>
        
        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="candidatesSearchPage"
            v-model:page-size="candidatesSearchPageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="candidatesSearchTotal"
            @size-change="handleCandidatesSearchSizeChange"
            @current-change="handleCandidatesSearchCurrentChange"
          />
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="assignCandidatesVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAssignCandidates" :loading="assignCandidatesLoading">
            确认分配
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 批量导入考生对话框 -->
    <el-dialog
      v-model="batchAssignVisible"
      title="批量导入考生"
      width="500px"
    >
      <div class="import-container">
        <el-upload
          class="upload-demo"
          drag
          action="#"
          :auto-upload="false"
          :on-change="handleFileChange"
          :limit="1"
          :file-list="fileList"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              请上传 Excel 文件 (xlsx, xls)，<el-link type="primary" @click="downloadTemplate">下载模板</el-link>
            </div>
          </template>
        </el-upload>
        
        <div class="import-actions">
          <el-button @click="batchAssignVisible = false">取消</el-button>
          <el-button type="primary" @click="submitBatchAssign" :loading="batchAssignLoading">
            开始导入
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>