<template>
  <div class="app-container">
    <div class="case-info">
      <el-descriptions class="margin-top" title="案件详情" :column="3" border>
        <template slot="extra">
          <el-button type="primary" size="small" @click="handleCaseUpdate">修改详情</el-button>
          <el-button type="primary" size="small" plain @click="caseFinished">标记完成</el-button>
        </template>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-collection" />
            案件名
          </template>
          {{ this.case.name }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-date" />
            开始日期
          </template>
          {{ this.case.started_date }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-date" />
            结束日期
          </template>
          {{ this.case.ended_date }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-circle-check" />
            完成状态
          </template>
          <el-tag size="small" :type="this.case.status | statusFilter">
            {{ this.case.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-notebook-2" />
            案件详细信息
          </template>
          {{ this.case.info }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <div class="case-tab">
      <el-tabs v-model="activeName">
        <el-tab-pane label="服务列表" name="first">
          <div class="list-header">
            <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleServCreate">添加服务</el-button>
          </div>
          <div class="list">
            <el-table
              v-loading="servListLoading"
              :data="serviceList"
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
              <el-table-column label="服务名称" prop="service_name" sortable>
                <template slot-scope="scope">
                  <el-link :underline="false" @click="goToDetail(scope.row)">{{ scope.row.service_name }}</el-link>
                </template>
              </el-table-column>
              <el-table-column label="服务类型" width="150px" align="center">
                <template slot-scope="scope">
                  <el-tag>{{ scope.row.type | servTypeFilter }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="开始日期" width="120px" align="center" prop="date_started" sortable>
                <template slot-scope="scope">
                  {{ scope.row.date_started }}
                </template>
              </el-table-column>
              <el-table-column label="结束日期" width="120px" align="center" prop="date_ended" sortable>
                <template slot-scope="scope">
                  {{ scope.row.date_ended }}
                </template>
              </el-table-column>
              <el-table-column label="完成状态" align="center" width="120px">
                <template slot-scope="scope">
                  <el-tag :type="scope.row.status | statusFilter">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" align="center" width="120px">
                <template slot-scope="scope">
                  <el-button type="danger" size="small" @click="deleteItem(scope.row)">删 除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        <el-tab-pane label="案件文档" name="second">
          <div class="doc-list">
            <div class="list-header">
              <el-button size="mini" type="primary" icon="el-icon-edit" @click="handleDocUpload">添加文档</el-button>
            </div>
            <div class="list">
              <el-table
                v-loading="docListLoading"
                :data="docList"
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
                <el-table-column label="上传时间" width="180px" align="center" prop="created_at" sortable="">
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
      </el-tabs>
    </div>
    <el-dialog :visible.sync="caseFormVisible" title="修改详情">
      <el-form ref="caseForm" :rules="caseRules" :model="caseTemp" label-position="left" label-width="100px" style="width: 400px; margin-left:50px;">
        <el-form-item label="案件名称" prop="case_name">
          <el-input v-model="caseTemp.case_name" />
        </el-form-item>
        <el-form-item label="案件信息" prop="case_info">
          <el-input v-model="caseTemp.case_info" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="caseFormVisible = false">
          取 消
        </el-button>
        <el-button type="primary" @click="updateCaseItem">
          确 认
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="servFormVisible" title="创建服务">
      <el-form ref="servForm" :rules="servRules" :model="servTemp" label-position="left" label-width="110px" style="width: 400px; margin-left:50px;">
        <el-form-item label="服务名称" prop="service_name">
          <el-input v-model="servTemp.service_name" />
        </el-form-item>
        <el-form-item label="服务类型" prop="type">
          <el-select v-model="servTemp.type" placeholder="请选择">
            <el-option
              v-for="item in servTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="供应商名" prop="provider_name">
          <el-input v-model="servTemp.provider_name" />
        </el-form-item>
        <el-form-item label="供应商联系方式" prop="provider_contact_info">
          <el-input v-model="servTemp.provider_contact_info" />
        </el-form-item>
        <el-form-item label="服务详细信息" prop="service_info">
          <el-input v-model="servTemp.service_info" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="servFormVisible = false">
          取 消
        </el-button>
        <el-button type="primary" @click="createServItem">
          确 认
        </el-button>
      </div>
    </el-dialog>
    <el-dialog :visible.sync="docFormVisible" title="上传文档">
      <el-form ref="docForm" :rules="docRules" :model="docTemp" label-position="left" label-width="110px" style="width: 400px; margin-left:50px;">
        <el-form-item label="文档类型" prop="type">
          <el-select v-model="docTemp.type" placeholder="请选择">
            <el-option
              v-for="item in docTypeOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="文档文件">
          <el-upload
            ref="upload"
            :auto-upload="false"
            :data="uploadData"
            :action="url"
            :headers="headers"
            :on-success="uploadSucceed"
          >
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="docFormVisible = false">
          取 消
        </el-button>
        <el-button type="primary" @click="docUpload">
          确 认
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getDateNow } from '@/utils/index'
import { getToken } from '@/utils/auth'
import {
  getCaseDetail, getServiceList, patchCaseDetail, postServDetail,
  deleteServItem, getCaseDocList, deleteDocItem, getCaseDoc
} from '@/api/case-mgmt'

const servTypeOptions = [
  { value: '11', label: '科技研究与试验发展' },
  { value: '12', label: '专业化技术' },
  { value: '13', label: '科技推广及相关' },
  { value: '14', label: '科技信息' },
  { value: '15', label: '科技金融' },
  { value: '16', label: '科技普及和宣传教育' },
  { value: '17', label: '综合科技' }
]

const docTypeOptions = [
  { value: '1', label: '需求文档' },
  { value: '2', label: '合同文档' }
  // { value: '3', label: '中间结果文档' },
  // { value: '4', label: '最终结果文档' }
]

const servTypeKeyValue = servTypeOptions.reduce((acc, cur) => {
  acc[cur.value] = cur.label
  return acc
}, {})

const docTypeKeyValue = docTypeOptions.reduce((acc, cur) => {
  acc[cur.value] = cur.label
  return acc
}, {})

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        '未完成': 'danger',
        '已完成': 'success'
      }
      return statusMap[status]
    },
    servTypeFilter(type) {
      return servTypeKeyValue[type]
    },
    docTypeFilter(type) {
      return docTypeKeyValue[type]
    }
  },
  data() {
    return {
      url: 'http://127.0.0.1:8000/api/case-doc/',
      activeName: 'first',
      case: {
        name: '',
        info: '',
        status: '',
        started_date: '',
        ended_date: ''
      },
      serviceList: [],
      servListLoading: true,
      docList: [],
      docListLoading: true,
      caseTemp: {
        case_name: '',
        case_info: ''
      },
      servTemp: {
        service_name: '',
        service_info: '',
        provider_name: '',
        provider_contact_info: '',
        type: ''
      },
      docTemp: {
        type: ''
      },
      caseRules: {
        case_name: [{ required: true, message: '请输入案件名', trigger: 'change' }]
      },
      servRules: {
        service_name: [{ required: true, message: '请输入服务名', trigger: 'change' }],
        provider_name: [{ required: true, message: '请输入提供商名', trigger: 'change' }],
        type: [{ required: true, message: '请选择服务类型', trigger: 'change' }]
      },
      docRules: {
        type: [{ required: true, message: '请选择文档类型', trigger: 'change' }]
      },
      caseFormVisible: false,
      servFormVisible: false,
      docFormVisible: false,
      servTypeOptions,
      docTypeOptions,
      headers: {
        Authorization: 'JWT ' + getToken()
      }
    }
  },
  computed: {
    uploadData: function() {
      return {
        type: this.docTemp.type,
        case_belonged: this.$route.params.case_id
      }
    }
  },
  created() {
    this.fetchCaseInfo()
    this.fetchServiceList()
    this.fetchDocList()
  },
  methods: {
    fetchCaseInfo() {
      getCaseDetail(this.$route.params.case_id).then((res) => {
        this.case.name = res.data.case_name
        this.case.info = res.data.case_info
        this.case.status = res.data.status
        this.case.started_date = res.data.date_started
        this.case.ended_date = res.data.date_ended
      })
    },
    fetchServiceList() {
      this.servListLoading = true
      getServiceList(this.$route.params.case_id).then((res) => {
        this.serviceList = res.data
        this.servListLoading = false
      })
    },
    fetchDocList() {
      this.docListLoading = true
      getCaseDocList({ case_id: this.$route.params.case_id }).then(res => {
        this.docList = res.data
        this.docListLoading = false
      })
    },
    resetCaseTemp() {
      this.caseTemp.case_name = this.case.name
      this.caseTemp.case_info = this.case.info
    },
    resetServTemp() {
      this.servTemp = {
        service_name: '',
        service_info: '',
        provider_name: '',
        provider_contact_info: '',
        type: ''
      }
    },
    handleCaseUpdate() {
      this.resetCaseTemp()
      this.caseFormVisible = true
      this.$nextTick(() => {
        this.$refs['caseForm'].clearValidate()
      })
    },
    updateCaseItem() {
      this.$refs['caseForm'].validate((valid) => {
        if (valid) {
          patchCaseDetail(this.$route.params.case_id, this.caseTemp).then(res => {
            this.caseFormVisible = false
            this.$message({
              showClose: true,
              message: '修改成功',
              type: 'success',
              duration: 1500
            })
            this.fetchCaseInfo()
          }).catch(err => {
            console.log(err)
            this.caseFormVisible = false
            this.$message({
              showClose: true,
              message: '修改失败',
              type: 'error',
              duration: 1500
            })
          })
        }
      })
    },
    caseFinished() {
      this.$confirm('确认完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        patchCaseDetail(this.$route.params.case_id, { state: true, date_ended: getDateNow() }).then(res => {
          this.$message({
            showClose: true,
            message: '标记成功',
            type: 'success',
            duration: 1500
          })
          this.fetchCaseInfo()
        }).catch(err => {
          this.$message({
            showClose: true,
            message: '标记失败',
            type: 'error',
            duration: 1500
          })
          console.log(err)
        })
      })
    },
    handleServCreate() {
      this.resetServTemp()
      this.servFormVisible = true
      this.$nextTick(() => {
        this.$refs['servForm'].clearValidate()
      })
    },
    createServItem() {
      this.$refs['servForm'].validate((valid) => {
        if (valid) {
          postServDetail(this.$route.params.case_id, this.servTemp).then(res => {
            this.servFormVisible = false
            this.$message({
              showClose: true,
              message: '添加成功',
              type: 'success',
              duration: 1500
            })
            this.fetchServiceList()
          }).catch(err => {
            console.log(err)
            this.servFormVisible = false
            this.$message({
              showClose: true,
              message: '添加失败',
              type: 'error',
              duration: 1500
            })
          })
        }
      })
    },
    goToDetail(row) {
      this.$router.push({
        name: 'ServDetail',
        params: { case_id: this.$route.params.case_id, serv_id: row.id }
      })
    },
    deleteItem(row) {
      this.$confirm('确认删除该服务？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async() => {
        const res = await deleteServItem(this.$route.params.case_id, row.id)
        if (res.status === 204) {
          this.$message({
            showClose: true,
            message: '删除成功',
            type: 'success',
            duration: 1500
          })
          this.fetchServiceList()
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
          this.fetchDocList()
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
    resetDocTemp() {
      this.docTemp.type = ''
    },
    handleDocUpload() {
      this.resetDocTemp()
      this.docFormVisible = true
      this.$nextTick(() => {
        this.$refs['docForm'].clearValidate()
      })
    },
    docUpload() {
      this.$refs['docForm'].validate(async(valid) => {
        if (valid) {
          this.$refs.upload.submit()
        } else {
          return false
        }
      })
    },
    uploadSucceed() {
      this.$message({
        showClose: true,
        message: '上传成功',
        type: 'success',
        duration: 1500
      })
      this.fetchDocList()
      this.docFormVisible = false
    },
    downloadDoc(row) {
      getCaseDoc(row.id).then(res => {
        const blob = new Blob([res.data], { type: 'application/octet-stream; charset=utf-8' })
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
</script>

<style scoped>
.case-info {
  margin-bottom: 15px
}
.list-header {
  margin-bottom: 10px
}
</style>
