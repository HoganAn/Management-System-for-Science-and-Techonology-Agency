<template>
  <div class="app-container">
    <div class="tab">
      <el-tabs v-model="activeName" type="border-card" @tab-click="handleTabClick">
        <el-tab-pane label="案件文档" name="1">
          <div class="doc-list">
            <div class="list">
              <el-table
                v-loading="caseDocListLoading"
                :data="caseDocList"
                element-loading-text="正在加载"
                border
                fit
                highlight-current-row
              >
                <el-table-column align="center" label="ID" width="50px">
                  <template slot-scope="scope">
                    {{ scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column label="文件名" prop="filename" sortable>
                  <template slot-scope="scope">
                    <el-link :underline="false" @click="downloadDoc(scope.row, 'case')">
                      {{ scope.row.filename }}
                    </el-link>
                  </template>
                </el-table-column>
                <el-table-column label="所属案件" width="250px" align="center" prop="case_name" sortable>
                  <template slot-scope="scope">
                    {{ scope.row.case_name }}
                  </template>
                </el-table-column>
                <el-table-column label="上传时间" width="180px" align="center" prop="created_at" sortable>
                  <template slot-scope="scope">
                    {{ scope.row.created_at }}
                  </template>
                </el-table-column>
                <el-table-column label="文档类型" width="150px" align="center">
                  <template slot-scope="scope">
                    <el-tag>
                      {{ scope.row.type | docTypeFilter }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" align="center" width="120px">
                  <template slot-scope="scope">
                    <el-button type="danger" size="small" @click="deleteDocItem(scope.row)">删 除</el-button>
                  </template>
                </el-table-column></el-table>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="服务文档" name="2">
          <div class="doc-list">
            <div class="list">
              <el-table
                v-loading="servDocListLoading"
                :data="servDocList"
                element-loading-text="正在加载"
                border
                fit
                highlight-current-row
              >
                <el-table-column align="center" label="ID" width="50px">
                  <template slot-scope="scope">
                    {{ scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column label="文件名" prop="filename" sortable>
                  <template slot-scope="scope">
                    <el-link :underline="false" @click="downloadDoc(scope.row)">
                      {{ scope.row.filename }}
                    </el-link>
                  </template>
                </el-table-column>
                <el-table-column label="所属服务" width="250px" align="center" prop="serv_name" sortable>
                  <template slot-scope="scope">
                    {{ scope.row.serv_name }}
                  </template>
                </el-table-column>
                <el-table-column label="上传时间" width="180px" align="center" prop="created_at" sortable>
                  <template slot-scope="scope">
                    {{ scope.row.created_at }}
                  </template>
                </el-table-column>
                <el-table-column label="文档类型" width="150px" align="center">
                  <template slot-scope="scope">
                    <el-tag>
                      {{ scope.row.type | docTypeFilter }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" align="center" width="120px">
                  <template slot-scope="scope">
                    <el-button type="danger" size="small" @click="deleteServDocItem(scope.row)">删 除</el-button>
                  </template>
                </el-table-column></el-table>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'
import {
  getCaseDocList, deleteDocItem, getCaseDoc,
  getServDocList, getServDoc, deleteServDocItem
} from '@/api/case-mgmt'

const caseDocTypeOptions = [
  { value: '1', label: '需求文档' },
  { value: '2', label: '合同文档' }
]

const servDocTypeOptions = [
  { value: '1', label: '需求文档' },
  { value: '2', label: '合同文档' },
  { value: '3', label: '中间结果文档' },
  { value: '4', label: '最终结果文档' }
]

const docTypeKeyValue = servDocTypeOptions.reduce((acc, cur) => {
  acc[cur.value] = cur.label
  return acc
}, {})

export default {
  filters: {
    docTypeFilter(type) {
      return docTypeKeyValue[type]
    }
  },
  data() {
    return {
      url: 'http://127.0.0.1:8000/api/case-doc/',
      activeName: '1',
      caseDocList: [],
      servDocList: [],
      caseDocListLoading: true,
      servDocListLoading: true,
      caseDocFormVisible: false,
      servDocFormVisible: false,
      caseDocTypeOptions,
      servDocTypeOptions,
      docTemp: {
        type: ''
      },
      docRules: {
        type: [{ required: true, message: '请选择文档类型', trigger: 'change' }]
      },
      headers: {
        Authorization: 'JWT ' + getToken()
      }
    }
  },
  created() {
    this.fetchCaseDocList()
  },
  methods: {
    handleTabClick(tab) {
      if (tab.index === '0') {
        this.fetchCaseDocList()
      } else {
        this.fetchServDocList()
      }
    },
    fetchCaseDocList() {
      this.caseDocListLoading = true
      getCaseDocList().then(res => {
        this.caseDocList = res.data
        this.caseDocListLoading = false
      })
    },
    fetchServDocList() {
      this.servDocListLoading = true
      getServDocList().then(res => {
        this.servDocList = res.data
        this.servDocListLoading = false
      })
    },
    deleteDocItem(row) {
      this.$confirm('确认删除该文档？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        const res = await deleteDocItem(row.id)
        if (res.status === 204) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success',
            duration: 1500
          })
          this.fetchCaseDocList()
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
    deleteServDocItem(row) {
      this.$confirm('确认删除该文档？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        const res = await deleteServDocItem(row.id)
        if (res.status === 204) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success',
            duration: 1500
          })
          this.fetchServDocList()
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
    downloadDoc(row, type) {
      if (type === 'case') {
        getCaseDoc(row.id).then(res => {
          const blob = new Blob([res.data], { type: 'application/octet-stream' })
          const fileNameEncode = res.headers['content-disposition'].split('filename=')[1]
          const fileName = decodeURIComponent(fileNameEncode)
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = fileName
          link.click()
          window.URL.revokeObjectURL(link.href)
        })
      } else {
        getServDoc(row.id).then(res => {
          const blob = new Blob([res.data], { type: 'application/octet-stream' })
          const fileNameEncode = res.headers['content-disposition'].split('filename=')[1]
          const fileName = decodeURIComponent(fileNameEncode)
          const link = document.createElement('a')
          link.href = window.URL.createObjectURL(blob)
          link.download = fileName
          link.click()
          window.URL.revokeObjectURL(link.href)
        })
      }
    }
  }
}
</script>

<style scoped>
.list-header {
  margin-bottom: 10px
}
</style>
