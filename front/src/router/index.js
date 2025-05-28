import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'

const DataManage = () => import('../views/DataManage.vue')
const Dummy = { template: '<div>功能开发中…</div>' }

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/data',
    component: DataManage,
    children: [
      { path: 'table', component: Dummy },
      { path: 'import', component: Dummy },
      { path: 'export', component: Dummy },
      { path: 'stat', component: Dummy }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
