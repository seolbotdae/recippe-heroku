<template>
  <v-container>
    마이페이지 기본 화면
    <v-btn @click="changePW">비밀번호 변경</v-btn>
  </v-container>
</template>

<script>
import router from '@/router/index.js';

export default {
  methods: {
    changePW() {
      router.push({
        path: "/email-auth",
        params: { 'nextPage': 1 }
      })
    }
  }
}
</script>