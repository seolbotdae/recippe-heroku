<template>
  <v-container>
    <v-form ref="form">
      <v-row>
        <v-col cols="4" offset="4">
          <v-card-title style="justify-content: center">이메일 인증</v-card-title>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" offset="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-text-field v-model="info.email" label="email"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2" offset="5">
          <v-btn @click="firstcheck" style="width: 100%">코드 전송하기</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" offset="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-otp-input length="6" type="number" v-model="info.code"></v-otp-input>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2" offset="5">
          <v-btn @click="secondcheck" style="width: 100%">인증하기</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" offset="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js'

export default {
  data() {
    return {
      info: {
        email: null,
        code: 0
      },
      nextPage: null
    }
  },
  mounted() {
    console.log("크리에이트 외않돌지?!?");
    console.log("route", router.params.nextPage);
    if(router.params.nextPage == 0) {
      this.nextPage = "/signup";
    } else if(router.params.nextPage == 1) {
      this.nextPage = "/mypage/changePassword";
    }
    console.log("params 메시지 받은내용", this.nextPage);
  },
  methods: {
    firstcheck() {
      const checkInfo = JSON.stringify({
        "email": this.info.email,
        "code": 0
      });
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
      });
      console.log(checkInfo);
      herokuAPI.secondcheck(checkInfo)
        .then(function (response) {
          console.log("secondcheck", response);
          if(response.status == 200) {
            console.log("코드 일치", this.nextPage);
            router.push({name: this.nextPage});
          }
        }) 
        .catch(function (e) {
          console.log(e);
        });
    }
  }
}
</script>