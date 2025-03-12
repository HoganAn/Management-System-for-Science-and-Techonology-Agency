<template>
  <div class="app-container">
    <div class="header">
      <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleCreate">添加案件</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="正在加载"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="50">
        <template slot-scope="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <el-table-column label="案件名称" prop="case_name" sortable>
        <template slot-scope="scope">
          <el-link :underline="false" @click="goToDetail(scope.row)">{{ scope.row.case_name }}</el-link>
        </template>
      </el-table-column>
      <el-table-column label="开始日期" width="150px" align="center" prop="date_started" sortable>
        <template slot-scope="scope">
          {{ scope.row.date_started }}
        </template>
      </el-table-column>
      <el-table-column label="结束日期" width="150px" align="center" prop="date_ended" sortable>
        <template slot-scope="scope">
          {{ scope.row.date_ended }}
        </template>
      </el-table-column>
      <el-table-column label="完成状态" align="center" width="150px">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">
            {{ scope.row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="150px">
        <template slot-scope="scope">
          <el-button type="danger" size="small" @click="deleteItem(scope.row)">删 除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="dialogFormVisible" title="创建案件">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
        <el-form-item label="案件名称" prop="case_name">
          <el-input v-model="temp.case_name" />
        </el-form-item>
        <el-form-item label="案件信息" prop="case_info">
          <el-input v-model="temp.case_info" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取 消
        </el-button>
        <el-button type="primary" @click="createItem()">
          确 认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getCaseList, deleteCaseItem, postCaseDetail } from '@/api/case-mgmt'
// import { format } from 'fecha'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        '未完成': 'danger',
        '已完成': 'success'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: [],
      listLoading: true,
      temp: {
        case_name: '',
        case_info: ''
      },
      dialogFormVisible: false,
      rules: {
        case_name: [{ required: true, message: '请输入案件名', trigger: 'change' }]
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getCaseList().then(responce => {
        this.list = responce.data
        this.listLoading = false
      })
    },
    goToDetail(row) {
      this.$router.push({
        name: 'CaseDetail',
        params: { case_id: row.id }
      })
    },
    resetTemp() {
      this.temp = {
        case_name: '',
        case_info: ''
      }
    },
    deleteItem(row) {
      this.$confirm('确认删除该案件？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        const res = await deleteCaseItem(row.id)
        if (res.status === 204) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success',
            duration: 1500
          })
          this.fetchData()
        } else {
          this.$message({
            showClose: true,
            message: '删除失败',
            type: 'error',
            duration: 1500
          })
        }
      })
    },
    handleCreate() {
      this.resetTemp()
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createItem() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          postCaseDetail(this.temp).then(res => {
            this.dialogFormVisible = false
            this.$message({
              showClose: true,
              message: '创建成功',
              type: 'success',
              duration: 1500
            })
            this.fetchData()
          }).catch(err => {
            console.log(err)
            this.dialogFormVisible = false
            this.$message({
              showClose: true,
              message: '创建失败',
              type: 'error',
              duration: 1500
            })
          })
        }
      })
    }
  }
}
</script>

<style scoped>
.header{
  margin-bottom: 10px
}
</style>
