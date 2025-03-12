<template>
  <!-- <div class="dashboard-container">
    <div class="dashboard-text">name: {{ nickname }}</div>
  </div> -->
  <div class="dashboard-container">
    <PanelGroup />
    <!-- <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="24">
        <el-card>
          <div class="welcome-msg">{{ getWelcomeMsg() + nickname }}</div>
        </el-card>
      </el-col>
    </el-row> -->
    <el-row :gutter="32">
      <el-col :xs="24" :sm="24" :lg="8">
        <el-card>
          <PieChart v-if="typeList.length > 0" :type-list="typeList" />
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="16">
        <el-card>
          <WordCloudChart v-if="keywordList.length > 0" :title="'个人关键词'" :keywords-list="keywordList" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import PieChart from './components/PieChart'
import WordCloudChart from './components/WordCloudChart'
import PanelGroup from './components/PanelGroup'
import { getUserKeywords, getTypeList } from '@/api/dashbord'

export default {
  name: 'Dashboard',
  components: {
    PieChart,
    WordCloudChart,
    PanelGroup
  },
  data() {
    return {
      keywordList: [],
      typeList: []
    }
  },
  computed: {
    ...mapGetters([
      'nickname'
    ])
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      // const res = await getUserKeywords()
      // this.keywordList = res.data
      getUserKeywords().then(res => {
        this.keywordList = res.data
      })
      getTypeList().then(res => {
        this.typeList = res.data
      })
    },
    getWelcomeMsg() {
      const date = new Date()
      const hours = date.getHours()
      let msg = ''
      if (hours >= 6 && hours < 11) {
        msg = '上午好，'
      } else if (hours >= 11 && hours < 14) {
        msg = '中午好，'
      } else if (hours >= 14 && hours < 18) {
        msg = '下午好，'
      } else {
        msg = '晚上好，'
      }
      return msg
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 32px;
  background-color: rgb(240, 242, 245);
  position: relative;
  .el-card {
    margin-bottom: 32px;
  }
  .welcome-msg {
    font-size: 24px;
  }
  .stats-data {
    float: right;
    margin-bottom: 15px;
  }
}
@media (max-width:1024px) {
  .el-card {
    padding: 8px;
  }
}
</style>
