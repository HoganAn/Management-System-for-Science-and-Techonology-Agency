<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/shine') // echarts theme
import resize from './mixins/resize'
export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    },
    typeList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'shine')
      this.chart.setOption({
        title: {
          text: '服务分类占比',
          x: 'center',
          textStyle: {
            fontWeight: 'bold'
          },
          padding: 0
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '0',
          data: [
            '科学研究与试验发展', '专业化技术', '科技推广及相关', '科技信息',
            '科技金融', '科技普及和宣传教育', '综合科技'
          ]
        },
        series: [
          {
            name: '服务类型',
            type: 'pie',
            roseType: 'radius',
            radius: [15, 95],
            center: ['50%', '45%'],
            data: this.typeList,
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    }
  }
}
</script>
