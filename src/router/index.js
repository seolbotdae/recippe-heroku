import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/components/Home'
import Create from '@/components/Create'
import Table from '@/components/Table'

Vue.use(Router); // vue 라우터 사용

const routes = [
  {
    path:'/',
    component:Home
  },
  {
    path:'/table',
    component:Table
  },
  {
    path:'/create',
    component:Create
  },
]

const router = new Router({
  mode: 'history',
  routes
})

export default router