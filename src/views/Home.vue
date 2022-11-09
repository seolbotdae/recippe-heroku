<template>
  <div>
    <div>app.vue</div>
    <v-btn><router-link to="/signup">회원가입</router-link></v-btn>
    <v-btn><router-link to="/login">로그인</router-link></v-btn>
    <v-btn><router-link to="/email-auth">이메일 인증</router-link></v-btn>
    <router-view />
  </div>
</template>