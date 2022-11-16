import Vue from 'vue';
import Router from 'vue-router';
// 레이아웃
import Empty from '@/EmptyLayout';
import Default from '@/DefaultLayout';

// 빈 레이아웃 화면
import Login from '@/views/Login';
import Signup from '@/views/Signup';
import EmailAuth from '@/views/EmailAuth';

// 기본 레이아웃 화면
import Home from '@/views/Home';
import Recipe from '@/views/Recipe';
import Photo from '@/views/Photo';
import MyPage from '@/views/MyPage';
// 레시피 게시판 관련 화면
import RecipeR from '@/views/Recipe/Recipe';
import CreateR from '@/views/Recipe/Create';
import LookupR from '@/views/Recipe/Lookup';
import EditR from '@/views/Recipe/Edit';
// 요리 사진 게시판 관련 화면
import PhotoP from '@/views/Photo/Photo';
import CreateP from '@/views/Photo/Create';
import LookupP from '@/views/Photo/Lookup';
import EditP from '@/views/Photo/Edit';
// 마이페이지 관련 화면
import MyPageM from '@/views/MyPage/MyPage';
import Refrigerator from '@/views/MyPage/Refrigerator';
import ChangeNickname from '@/views/MyPage/ChangeNickname';
import ChangePassword from '@/views/MyPage/ChangePassword';

Vue.use(Router); // vue 라우터 사용
const routes = [
  {
    path: '/',
    component: Default,
    children: [
      {
        path: '/',
        name: 'home',
        component: Home
      },
      {
        path: '/recipe',
        component: Recipe,
        children: [
          {
            path: '/recipe',
            name: 'recipe',
            component: RecipeR
          },
          {
            path: '/recipe/create',
            name: 'createR',
            component: CreateR
          },
          {
            path: '/recipe/lookup',
            name: 'lookupR',
            component: LookupR
          },
          {
            path: '/recipe/edit',
            name: 'editR',
            component: EditR
          },
        ]
      },
      {
        path: '/photo',
        component: Photo,
        children: [
          {
            path: '/photo',
            name: 'photo',
            component: PhotoP
          },
          {
            path: '/photo/create',
            name: 'createP',
            component: CreateP
          },
          {
            path: '/photo/lookup',
            name: 'lookupP',
            component: LookupP
          },
          {
            path: '/photo/edit',
            name: 'editP',
            component: EditP
          },
        ]
      },
      {
        path: '/mypage',
        component: MyPage,
        children: [
          {
            path: '/mypage',
            name: 'mypage',
            component: MyPageM
          },
          {
            path: '/mypage/refrigerator',
            name: 'refrigerator',
            component: Refrigerator
          },
          {
            path: '/changeNickname',
            name: 'changeNickname',
            component: ChangeNickname
          },
          {
            path: '/changePassword',
            name: 'changePassword',
            component: ChangePassword
          },
        ]
      }
    ]
  },
  {
    path: '/',
    component: Empty,
    children: [
      {
        path: '/login',
        name: 'login',
        component: Login
      },
      {
        path: '/signup',
        name: 'signup',
        component: Signup
      },
      {
        path: '/email-auth',
        name: 'email-auth',
        component: EmailAuth
      },
    ]
  }
]

const router = new Router({
  mode: 'history',
  routes
})

export default router