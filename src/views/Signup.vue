<template>
  <v-container justify-center align-center>
    <v-form ref="form">
      <v-row>
        <v-col cols="6">
          <v-text-field v-model="info.id" label="id"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-text-field v-model="info.nick" label="nickname"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-text-field v-model="info.pw" label="password"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-text-field v-model="info.pwcheck" label="check password"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3" offset="3">
          <v-btn><router-link to="/login">돌아가기</router-link></v-btn>
        </v-col>
        <v-col cols="3" offset="3">
          <v-btn @click.enter="signup">회원가입</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default {
  data() {
    return {
      info: {
        id: null,
        nick: null,
        pw: null,
        pwcheck: null
      }
    }
  },
  methods: {
    signup() {
      const signupInfo = {
        
      }
      console.log(signupInfo);
      JSON.parse(signupInfo);
      herokuAPI.signup(signupInfo)
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