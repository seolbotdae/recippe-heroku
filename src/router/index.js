import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home'
import Login from '@/views/Login'
import Signup from '@/views/Signup'
import EmailAuth from '@/views/EmailAuth'

Vue.use(Router); // vue 라우터 사용

const routes = [
  {
    path:'/',
    component:Home
  },
  {
    path:'/login',
    component:Login
  },
  {
    path:'/signup',
    component:Signup
  },
  {
    path:'/email-auth',
    component:EmailAuth
  },
]

const router = new Router({
  mode: 'history',
  routes
})

export default router