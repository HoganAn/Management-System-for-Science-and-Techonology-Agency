<template>
  <div class="app-container">
    <div class="serv-info">
      <el-descriptions class="margin-top" title="服务详情" :column="3" border>
        <template slot="extra">
          <el-button type="primary" size="small" @click="handleServUpdate">修改详情</el-button>
          <el-button type="primary" size="small" plain @click="servFinished">标记完成</el-button>
        </template>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-collection" />
            服务名
          </template>
          {{ this.serv.name }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-date" />
            开始日期
          </template>
          {{ this.serv.started_date }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-date" />
            结束日期
          </template>
          {{ this.serv.ended_date }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-collection-tag" />
            服务类型
          </template>
          <el-tag size="small">
            {{ this.serv.type | typeFilter }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-circle-check" />
            完成状态
          </template>
          <el-tag size="small" :type="this.serv.status | statusFilter">
            {{ this.serv.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-notebook-2" />
            服务详细信息
          </template>
          {{ this.serv.info }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-office-building" />
            供应商名
          </template>
          {{ this.serv.provider_name }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template slot="label">
            <i class="el-icon-mobile-phone" />
            供应商联系方式
          </template>
          {{ this.serv.provider_contact_info }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <div class="serv-tab">
      <el-tabs v-model="activeName">
        <el-tab-pane label="服务文档" name="first">
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
      </el-tabs>
    </div>
    <el-dialog :visible.sync="servFormVisible" title="修改详情">
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
        <el-form-item label="服务信息" prop="service_info">
          <el-input v-model="servTemp.service_info" :autosize="{ minRows: 2, maxRows: 4 }" type="textarea" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="servFormVisible = false">
          取 消
        </el-button>
        <el-button type="primary" @click="updateServItem">
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
import { getServDetail, patchServDetail, getServDocList, deleteServDocItem, getServDoc } from '@/api/case-mgmt'

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
  { value: '2', label: '合同文档' },
  { value: '3', label: '中间结果文档' },
  { value: '4', label: '最终结果文档' }
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
    typeFilter(type) {
      return servTypeKeyValue[type]
    },
    docTypeFilter(type) {
      return docTypeKeyValue[type]
    }
  },
  data() {
    return {
      url: 'http://127.0.0.1:8000/api/serv-doc/',
      activeName: 'first',
      serv: {
        name: '',
        info: '',
        status: '',
        started_date: '',
        ended_date: '',
        type: '',
        provider_name: '',
        provider_contact_info: ''
      },
      docList: [],
      docListLoading: true,
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
      servRules: {
        service_name: [{ required: true, message: '请输入服务名', trigger: 'change' }],
        provider_name: [{ required: true, message: '请输入提供商名', trigger: 'change' }],
        type: [{ required: true, message: '请选择服务类型', trigger: 'change' }]
      },
      docRules: {
        type: [{ required: true, message: '请选择文档类型', trigger: 'change' }]
      },
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
        serv_belonged: this.$route.params.serv_id
      }
    }
  },
  created() {
    this.fetchServInfo()
    this.fetchDocList()
  },
  methods: {
    fetchServInfo() {
      getServDetail(this.$route.params.case_id, this.$route.params.serv_id).then((res) => {
        this.serv.name = res.data.service_name
        this.serv.info = res.data.service_info
        this.serv.status = res.data.status
        this.serv.type = res.data.type
        this.serv.started_date = res.data.date_started
        this.serv.ended_date = res.data.date_ended
        this.serv.provider_name = res.data.provider_name
        this.serv.provider_contact_info = res.data.provider_contact_info
      })
    },
    fetchDocList() {
      this.docListLoading = true
      getServDocList({ serv_id: this.$route.params.serv_id }).then(res => {
        this.docList = res.data
        this.docListLoading = false
      })
    },
    resetServTemp() {
      this.servTemp = {
        service_name: this.serv.name,
        service_info: this.serv.info,
        provider_name: this.serv.provider_name,
        provider_contact_info: this.serv.provider_contact_info,
        type: this.serv.type
      }
    },
    handleServUpdate() {
      this.resetServTemp()
      this.servFormVisible = true
      this.$nextTick(() => {
        this.$refs['servForm'].clearValidate()
      })
    },
    servFinished() {
      this.$confirm('确认完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        patchServDetail(this.$route.params.case_id, this.$route.params.serv_id,
          { state: true, date_ended: getDateNow() }).then(res => {
          this.$message({
            showClose: true,
            message: '标记成功',
            type: 'success',
            duration: 1500
          })
          this.fetchServInfo()
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
    updateServItem() {
      this.$refs['servForm'].validate((valid) => {
        if (valid) {
          patchServDetail(this.$route.params.case_id, this.$route.params.serv_id, this.servTemp).then(res => {
            this.servFormVisible = false
            this.$message({
              showClose: true,
              message: '修改成功',
              type: 'success',
              duration: 1500
            })
            this.fetchServInfo()
          }).catch(err => {
            console.log(err)
            this.servFormVisible = false
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
    deleteDocItem(row) {
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
</script>

<style scoped>
.serv-info {
  margin-bottom: 15px
}
.list-header {
  margin-bottom: 10px
}
</style>
