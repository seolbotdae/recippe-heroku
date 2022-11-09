<template>
  <v-container>
    <v-text-field v-model="info.email" label="email"></v-text-field>
    <v-btn @click="firstcheck">코드 전송하기</v-btn>
    <v-otp-input length="6" v-model="info.code"></v-otp-input>
    <v-btn @click="secondcheck">인증하기</v-btn>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default {
  data() {
    return {
      info: {
        email: null,
        code: 0
      }
    }
  },
  methods: {
    firstcheck() {
      const checkInfo = JSON.stringify({
        "email": this.info.email,
        "code": 0
      })
      console.log(checkInfo);
      JSON.parse(checkInfo);
      herokuAPI.firstcheck(checkInfo)
        .then(function (response) {
          console.log("firstcheck", response);
        }) 
        .catch(function (e) {
          console.log(e);
        });
    },
    secondcheck() {
      const codenum = Number(this.info.code);
      const checkInfo = JSON.stringify({
        "email": this.info.email,
        "code": codenum
      })
      console.log(checkInfo);
      JSON.parse(checkInfo);
      herokuAPI.secondcheck(checkInfo)
        .then(function (response) {
          console.log("secondcheck", response);
        }) 
        .catch(function (e) {
          console.log(e);
        });
    }
  }
}
</script>