<template>
  <v-container>
    마이페이지 기본 화면
    <v-btn to="{name: '/email-auth', query: { nextpage: '/mypage/changepassword' }}">회원가입</v-btn>
  </v-container>
</template>