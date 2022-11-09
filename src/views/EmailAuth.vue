<template>
  <v-app>
    <v-text-field v-model="info.email" label="email"></v-text-field>
    <v-text-field v-model="info.code" label="code"></v-text-field>
    <v-btn @click.enter="firstcheck">인증하기</v-btn>
  </v-app>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default {
  data() {
    return {
      info: {
        email: null,
        code: null
      }
    }
  },
  methods: {
    firstcheck() {
      const firstcheckInfo = JSON.stringify({
        "email": this.info.email,
        "code": this.info.code
      })
      console.log(firstcheckInfo);
      herokuAPI.firstcheck(firstcheckInfo)
        .then(function (response) {
          console.log("firstcheck", response);
        }) 
        .catch(function (e) {
          console.log(e);
        });
    }
  }
}
</script>