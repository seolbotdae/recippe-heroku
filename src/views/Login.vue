<template>
  <v-app>
    <v-text-field v-model="info.id" label="id"></v-text-field>
    <v-text-field v-model="info.pw" label="password"></v-text-field>
    <v-checkbox v-model="info.al" label="자동 로그인"></v-checkbox>
    <v-btn @click.enter="login">login</v-btn>
    <v-btn><router-link to="/signup">회원가입</router-link></v-btn>
  </v-app>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default {
  data() {
    return {
      info: {
        id: null,
        pw: null,
        al: false
      }
    }
  },
  methods: {
    login() {
      const loginInfo = JSON.stringify({
        "nickname": null,
        "uid": this.info.id,
        "password": this.info.pw,
        "email": null,
        "auto_login": this.info.al,
      });
      console.log(loginInfo);
      JSON.parse(loginInfo);
      herokuAPI.login(loginInfo)
        .then(function (response) {
          console.log("login", response);
        }) 
        .catch(function (e) {
          console.log(e);
        });
    }
  }
}
</script>