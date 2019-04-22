<template>
  <div>
    <v-chart id="dict" :options="dict" @dblclick="dbclick"/>
  </div>
</template>

<script>
import 'echarts/lib/chart/graph'
import dict from '../assets/schema'

export default {
  name: 'HelloWorld',

  data () {
    let categories = []
    let data = []
    let links = []
    let nodes = []
    for (let values of Object.values(dict)) {
      if (values.id && !['_terms', '_definitions'].includes(values.id)) {
        nodes.push(values)
      }
      if (!categories.includes(values.category)) {
        categories.push({name: values.category})
      }
    }
    nodes.sort((x, y) => {
      if (['program', 'project'].includes(x.id)) return 1
      if (['program', 'project'].includes(y.id)) return -1
      return x.category === y.category ? x.id < y.id : x.category < y.category
    })
    let lastCategory = ''
    // let x = 100
    // let y = 100
    for (let values of nodes) {
      let node = {
        name: values.id,
        category: values.category
      }
      if (node.category === 'administrative') {
        node.symbolSize = 30
      }
      if (node.name === 'program') {
        node.fixed = true
        node.symbolSize = 50
        node.x = 500
        node.y = 50
      }
      if (node.name === 'project') {
        node.fixed = true
        node.symbolSize = 50
        node.x = 500
        node.y = 150
      }
      // node.x = x
      // node.y = y
      // x += 100
      if (node.category !== lastCategory) {
        // y += 100
        lastCategory = node.category
        // x = 100
      }
      data.push(node)
      if (values.links) {
        for (let link of values.links) {
          if (link.target_type) {
            links.push({
              source: values.id,
              target: link.target_type
            })
          } else if (link.subgroup) {
            for (let slink of link.subgroup) {
              links.push({
                source: values.id,
                target: slink.target_type
              })
            }
          }
        }
      }
    }
    return {
      dict: {
        series: [
          {
            type: 'graph',
            layout: 'force',
            roam: true,
            data: data,
            links: links,
            categories: categories,
            draggable: true,
            focusNodeAdjacency: true,
            force: {
              // initLayout: 'circular',
              repulsion: 100,
              edgeLength: [200, 200]
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3
            }
          }
        ]
      }
    }
  },

  created () {
  },

  methods: {
    dbclick (args) {
      let i = this.dict.series[0].data.findIndex(node => node.name === args.data.name)
      this.dict.series[0].data[i].fixed = !this.dict.series[0].data[i].fixed
      console.log(this.dict.series[0].data[i])
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #dict {
    width: 100vw;
    height: 100vh;
  }
</style>
