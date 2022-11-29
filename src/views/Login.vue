<template>
  <v-container>

    <v-form ref="form" v-model="valid" lazy-validation>
      <v-row>
        <v-col cols="4" offset="4">
          <v-card-title style="justify-content: center">로그인</v-card-title>
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
            v-model="info.pw" 
            label="password"
            type="password"
            :rules="pw_rule"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="3" offset="4">
          <v-checkbox v-model="info.al" label="자동 로그인"></v-checkbox>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="auto">
          <v-btn @click="signup">회원가입</v-btn>
        </v-col>
        <v-col cols="2">
          <v-btn @click="login" style="width: 100%">login</v-btn>
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
        headerTitle = "계정 정보 없음"
        btn1Title="확인"
        :btn2=false
        @hide="hideDialog"
        @submit="checkDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>아이디 또는 비밀번호를<br> 잘못 입력했습니다.</div>
        </template>
      </popup-dialog>
    </v-dialog>
    
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
import PopupDialog from '@/components/popup.vue';

export default{
  components: {
    PopupDialog
  },
  data(){
    return{
      valid: true,
      popupDialog: false,

      snackbar: false,
      snackbarContents: "",

      info: {
        id: null,
        pw: null,
        al: false
      },

    // 유효성 검사
      id_rule: [
        v => !!v || '아이디를 입력하세요.',
      ],
      pw_rule: [
        v => !!v || '비밀번호를 입력하세요.',
      ],
    }
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
    login(){
      let vm = this;
      const validate = this.$refs.form.validate();
      if(!validate) {
        vm.snackbarContents = "아이디와 비밀번호를 모두 입력해 주세요."
        vm.snackbar = true;
        return;
      }
      
      let hashedPWD = this.hashing(vm.info.pw);

      const loginInfo = JSON.stringify({
        "nickname": null,
        "uid": vm.info.id,
        "password": hashedPWD,
        "email": null,
        "auto_login": vm.info.al,
      });
      const auto_login = vm.info.al;
      herokuAPI.login(loginInfo)
        .then(function (response) {
          if(response.status == 200) {
            const dataString = JSON.stringify({
              "nickname": response.data.nickname,
              "uid": response.data.uid,
              "password": response.data.password,
              "email": response.data.email,
              "auto_login": auto_login,
            });
            localStorage.setItem("UserInfo", dataString);
            sessionStorage.setItem("running", "true")
            router.push({name: 'home'});
          }
        })
        .catch(function (e) {
          if(e.response.status == 400) {
            console.log("400 아이디 또는 비밀번호 불일치");
            vm.snackbarContents = "아이디 또는 비밀번호가 잘못되었습니다."
            vm.snackbar = true;
          } else if(e.response.status == 500) {
            console.log("500 Unknown error");
            vm.snackbarContents = "알 수 없는 이유로 로그인에 실패했습니다."
            vm.snackbar = true;
          }
        });
    },
    signup(){
      router.push({
        path: "/email-auth/0",
      })
    },
    hashing(content){
      var result = "";
      for(let i = 0; i < content.length; i++){
        result += String.fromCharCode(Number(content.charCodeAt(i))+1);
      }
      return result;
    }
  }
}
</script>