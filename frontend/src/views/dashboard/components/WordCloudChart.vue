<template>
  <div :class="className" :style="{ height: height, width: width }" />
</template>

<script>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
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
    title: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      default: 'keyword_chart'
    },
    keywordsList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      chart: null
    }
  },
  // watch: {
  //   keywordList: {
  //     deep: true,
  //     handler() {
  //       this.initChart()
  //     }
  //   }
  // },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.charts) {
      return
    }
    this.chart.dispose()
    this.chart = []
    this.keywordList = []
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el)
      const option = {
        title: {
          text: this.title,
          x: 'center'
        },
        series: [{
          type: 'wordCloud',

          // The shape of the "cloud" to draw.
          shape: 'circle',

          // Keep aspect ratio of maskImage or 1:1 for shapes
          keepAspect: false,

          // A silhouette image which the white area will be excluded from drawing texts.
          // The shape option will continue to apply as the shape of the cloud to grow.
          // maskImage: maskImage,

          // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
          // Default to be put in the center and has 75% x 80% size.
          left: 'center',
          top: 'center',
          width: '85%',
          height: '80%',
          right: null,
          bottom: null,

          // Text size range which the value in data will be mapped to.
          // Default to have minimum 12px and maximum 60px size.
          sizeRange: [14, 60],

          // Text rotation range and step in degree.
          rotationRange: [0, 0],
          rotationStep: 0,

          // Size of the grid in pixels for marking the availability of the canvas
          // the larger the grid size, the bigger the gap between words.
          gridSize: 3,

          // Set to true to allow word being draw partly outside of the canvas.
          // Allow word bigger than the size of the canvas to be drawn
          drawOutOfBound: true,

          // If perform layout animation.
          // NOTE disable it will lead to UI blocking when there is lots of words.
          layoutAnimation: true,

          // Global text style
          textStyle: {
            fontFamily: 'Hiragino Sans GB',
            fontWeight: 'bold',
            // Color can be a callback function or a color string
            color: function(e) {
              // Random color
              // return 'rgb(' + [
              //   Math.round(Math.random() * 160),
              //   Math.round(Math.random() * 160),
              //   Math.round(Math.random() * 160)
              // ].join(',') + ')'
              const colors = [
                '#2ec7c9', '#b6a2de', '#5ab1ef', '#ffb980', '#d87a80',
                '#8d98b3', '#e5cf0d', '#97b552', '#95706d', '#dc69aa',
                '#07a2a4', '#9a7fd1', '#588dd5', '#f5994e', '#c05050',
                '#59678c', '#c9ab00', '#7eb00a', '#6f5553', '#c14089'
              ]
              return colors[e.dataIndex % 20]
            }
          },
          emphasis: {
            focus: 'self',
            textStyle: {
              textShadowBlur: 3,
              textShadowColor: '#333'
            }
          },

          // Data is an array. Each array item must have name and value property.
          data: this.keywordsList
        }]
      }
      this.chart.setOption(option)
    }
  }
}
</script>

<style>

</style>
