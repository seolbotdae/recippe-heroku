<template>
  <v-container>
    <v-form>
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
          <v-form ref="form" v-model="valid" lazy-validation>
            <v-text-field 
              v-model="info.email" 
              label="이메일을 입력하세요"
              :rules="email_rule"
              required
              :disabled="sendCode"
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

    <v-snackbar v-model="snackbar" timeout="3000">
      {{ snackbarContents }}
      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>

  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default{
  data() {
    return {
      valid: true,
      info: {
        email: null,
        code: ""
      },
      next: null,
      snackbar: false,
      snackbarContents: "",
      sendCode: false,

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
      let vm = this;
      const validate = this.$refs.form.validate();
      if(!validate) {
        vm.snackbarContents = "잘못된 형식의 입력입니다."
        vm.snackbar = true;
        return;
      }
      const checkInfo = JSON.stringify({
        "email": this.info.email,
        "code": 0
      });
      console.log(checkInfo);
      JSON.parse(checkInfo);
      herokuAPI.firstcheck(checkInfo)
        .then(function (response) {
          console.log("firstcheck", response);
          vm.snackbarContents = "이메일을 전송했습니다."
          vm.snackbar = true;
          vm.sendCode = true;
        })
        .catch(function (e) {
          if(e.response.status == 501) {
            console.log("501 전송실패");
            vm.snackbarContents = "이메일 전송에 실패했습니다."
            vm.snackbar = true;
          } else if(e.response.status == 404) {
            console.log("404 존재하지 않는 이메일");
            vm.snackbarContents = "존재하지 않는 이메일입니다."
            vm.snackbar = true;
          }
        });
    },
    secondcheck() {
      let vm = this;
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
          if(e.response.status == 400) {
            console.log("400 잘못된 코드");
            vm.snackbarContents = "잘못된 인증코드입니다."
            vm.snackbar = true;
          } else if(e.response.status == 500) {
            console.log("500 등록 실패");
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
          }
        });
    }
  },
}
</script>