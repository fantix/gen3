// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ECharts from 'vue-echarts'
import 'echarts-gl'
import App from './App'
import router from './router'

Vue.component('v-chart', ECharts)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
