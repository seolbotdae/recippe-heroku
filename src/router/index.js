import Vue from 'vue';
import Router from 'vue-router';
import Empty from '@/EmptyLayout'
import Default from '@/DefaultLayout'
import Home from '@/views/Home'
import Login from '@/views/Login'
import Signup from '@/views/Signup'
import EmailAuth from '@/views/EmailAuth'

Vue.use(Router); // vue 라우터 사용
const routes = [
  {
    path: '/',
    component: Default,
    children: [
      {
        path:'/',
        name: 'home',
        component:Home
      },
    ]
  },
  {
    path: '/',
    component: Empty,
    children: [
      {
        path:'/login',
        name: 'login',
        component:Login
      },
      {
        path:'/signup',
        name: 'signup',
        component:Signup
      },
      {
        path:'/email-auth',
        name: 'email-auth',
        component:EmailAuth
      },
    ]
  }
]

const router = new Router({
  mode: 'history',
  routes
})

export default router