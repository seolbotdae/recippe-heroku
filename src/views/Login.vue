<template>
  <v-container>

    <v-form ref="form">
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
          <v-text-field v-model="info.id" label="id"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" offset="4">
          <v-text-field v-model="info.pw" label="password"></v-text-field>
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
        btnTitle="확인"
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
  data(){
    return{
      popupDialog: false,
      info: {
        id: null,
        pw: null,
        al: false
      }
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
      const loginInfo = JSON.stringify({
        "nickname": null,
        "uid": vm.info.id,
        "password": vm.info.pw,
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
            router.push({name: 'home'});
          }
        }) 
        .catch(function (e) {
          if(e.response.status == 400) {
            console.log("400 error");
            vm.showDialog();
          }
        });
    },
    signup(){
      router.push({
        path: "/email-auth/0",
      })
    }
  }
}
</script>