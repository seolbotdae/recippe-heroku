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
          <v-form ref="form" lazy-validation>
            <v-text-field 
              v-model="info.email" 
              label="이메일을 입력하세요"
              :rules="email_rule"
              required
            ></v-text-field>
          </v-form>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2" offset="5">
          <v-btn @click="firstcheck()" style="width: 100%">코드 전송하기</v-btn>
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
          <v-btn @click="secondcheck()" style="width: 100%">인증하기</v-btn>
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
import router from '@/router/index.js';

export default{
  data() {
    return {
      info: {
        email: null,
        code: ""
      },
      next: null,

    // 유효성 검사
      email_rule: [
        v => !!v || '인증코드를 받을 이메일을 입력하세요.',
        v => /^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(v) || '올바른 이메일을 입력하세요.',
      ]
    }
  },
  created() {
    console.log("route", this.$route.params.id);
    if(this.$route.params.id == 0) {
      this.next = "signup";
    } else if(this.$route.params.id == 1) {
      this.next = "changePassword";
    }
    console.log("params 메시지 받은내용", this.next);
  },
  methods: {
    firstcheck() {
      const validate = this.$refs.form.validate();
      if(validate) {
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
      }
    },
    secondcheck() {
      const codenum = Number(this.info.code);
      const checkInfo = JSON.stringify({
        "email": this.info.email,
        "code": codenum
      });
      const email = this.info.email;
      const next = this.next;
      console.log(checkInfo);
      herokuAPI.secondcheck(checkInfo)
        .then(function (response) {
          console.log("secondcheck", response);
          if(response.status == 200) {
            console.log("코드 일치", next);
            if(next == 'signup') {
              localStorage.setItem("email", email);
            }
            router.push({name: next});
          }
        }) 
        .catch(function (e) {
          console.log(e);
        });
    }
  }
}
</script>