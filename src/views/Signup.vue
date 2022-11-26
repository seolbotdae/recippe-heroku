<template>
  <v-container >
    <v-form ref="form" lazy-validation>
      <v-row>
        <v-col cols="4" offset="4">
          <v-card-title style="justify-content: center">레쉽피 회원가입</v-card-title>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="6" offset="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="4" offset="4">
          <v-text-field 
            v-model="info.id" 
            label="id"
            :rules="id_rule"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-text-field 
            v-model="info.nick" 
            label="nickname"
            :rules="nn_rule"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-text-field 
            v-model="info.pw" 
            label="password"
            :rules="pw_rule"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-text-field 
            v-model="info.pwcheck" 
            label="check password"
            :rules="pwch_rule"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto">
          <v-btn to="/login">돌아가기</v-btn>
        </v-col>
        <v-col cols="2">
          <v-btn @click="signup" style="width: 100%">회원가입</v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="6" offset="3">
          <v-divider></v-divider>
        </v-col>
      </v-row>
    </v-form>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=title
        btn1Title="확인"
        :btn2=false
        @hide="hideDialog"
        @submit="checkDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>중복된 {{text}} 입니다.</div>
        </template>
      </popup-dialog>
    </v-dialog>
    <!-- 팝업창 형식 -->

  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';
import PopupDialog from '@/components/popup.vue';

export default{
  components: {
    PopupDialog
  },
  data() {
    return {
      popupDialog: false,
      title: "",
      text: "",
      info: {
        email: null,
        id: null,
        nick: null,
        pw: null,
        pwcheck: null,
      },

    // 유효성 검사
      id_rule: [
        v => !!v || '아이디를 입력하세요.',
        v => !(v && v.length < 6) || '아이디는 6자 이상이여야 합니다.',
      ],
      nn_rule: [
        v => !!v || '닉네임을 입력하세요.',
      ],
      pw_rule: [
        v => !!v || '새로운 비밀번호를 입력하세요.',
        v => !(v && v.length < 6) || '비밀번호는 6자 이상이여야 합니다.',
        v => /^[a-z0-9!?@<>]*$/.test(v) || '비밀번호는 영어 소문자, 숫자, 특수문자(!, ?, @, <, >)만 사용 가능합니다.',
        v => /^.*[a-z]+.*$/.test(v) || '비밀번호에는 영어 소문자가 포함되어야 합니다.',
        v => /^.*[0-9]+.*$/.test(v) || '비밀번호에는 숫자가 포함되어야 합니다.',
        v => /^.*[!?@<>]+.*$/.test(v) || '비밀번호에는 특수문자(!, ?, @, <, >)가 포함되어야 합니다.',
      ],
      pwch_rule: [
        v => !!v || '비밀번호 확인을 입력하세요.',
        v => v === this.user.pw || '비밀번호가 일치하지 않습니다.',
      ],
    }
  },
  created() {
    this.info.email = localStorage.getItem("email");
    console.log("로컬스토리지에서 이메일 받아오기", this.info.email);
    localStorage.removeItem("email");
  },
  methods: {
    showDialog(){ // 팝업창 보이기
      this.popupDialog = true
    },
    hideDialog(){ // 팝업창 숨기기
      this.popupDialog = false
    },
    checkDialog(){ // 팝업창 버튼 클릭시
      // 확인 버튼 클릭시 동작 걸기
      this.hideDialog();
    },
    signup() {
      const validate = this.$refs.form.validate();
      if(validate) {
        let vm = this;
        const signupInfo = JSON.stringify({
          "nickname": this.info.nick,
          "uid": this.info.id,
          "password": this.info.pw,
          "email": this.info.email,
          "auto_login": false,
        });
        console.log(signupInfo);
        herokuAPI.signup(signupInfo)
          .then(function (response) {
            console.log(response)
            if(response.status == 200) {
              console.log("회원가입 성공")
              router.push({name: 'login'});
            }
          }) 
          .catch(function (e) {
            if(e.response.status == 400) {
              console.log("400 error");
              vm.text = "아이디";
              vm.title = "아이디 중복";
              vm.showDialog();
            } else if(e.response.status == 401) {
              console.log("401 error");
              vm.text = "닉네임";
              vm.title = "닉네임 중복";
              vm.showDialog();
            } else if(e.response.status == 402) {
              console.log("402 error");
              vm.text = "아이디, 닉네임";
              vm.title = "아이디, 닉네임 중복";
              vm.showDialog();
            }
          });
      }
    },
  }
}
</script>