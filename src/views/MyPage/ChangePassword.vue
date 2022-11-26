<template>
  <v-container>
    <v-layout>
      <v-row justify="center">
        <v-col cols="8">
          <v-card color="#f5efe6" height="800">
            <v-card color="#f5efe6" height="200" flat>
              
            </v-card>
            <v-layout>
              <v-row justify="center">
                <v-col class="col-xl-4 col-md-6">
                  <v-card color="#fefefe" height="400" rounded="xl">
                    <v-card-title id="title" class="pa-10 justify-center fontsize">비밀번호 변경</v-card-title>

                    <v-col>
                      <v-text-field v-model="user.pw" filled label="새 비밀번호" placeholder="새로운 비밀번호 입력."></v-text-field>
                      <v-text-field v-model="user.pwcheck" filled label="비밀번호 확인" placeholder="비밀번호 확인."></v-text-field>
                    </v-col>

                    
                    <v-col>
                      <v-row justify="center">
                        <v-card-actions>
                          <v-btn outlined width="100" to="/mypage">취소</v-btn>
                        </v-card-actions>
                        <v-card-actions>
                          <v-btn outlined width="100" @click="PWchange()">변경</v-btn>
                        </v-card-actions>
                      </v-row>
                      
                    </v-col>
                  </v-card>
                </v-col>
              </v-row>
            </v-layout>
            
          </v-card>
        </v-col>
      </v-row>
    </v-layout>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=headerTitle
        btn1Title="확인"
        :btn2=false
        @hide="hideDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div> {{ content1 }} </div>
        </template>
      </popup-dialog>
    </v-dialog>

  </v-container>
</template>

<style>
  #title{
    font-weight: 700;
    font-size: 2em;
  }

</style>

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
      headerTitle: "",
      content1: "",
      user: {
        email: '',
        id: '',
        nickname: '',
        pw: '',
        pwcheck: '',
        al: ''
      },
      nickname: ''
    };
  },
  created() {
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    this.nickname = UserInfo.nickname
    this.user.id = UserInfo.uid
    this.user.email = UserInfo.email
    this.user.al = UserInfo.auto_login
  },
  methods: {
    showDialog(){ // 팝업창 보이기
      this.popupDialog = true
    },
    hideDialog(){ // 팝업창 숨기기
      this.popupDialog = false
    },
    changeFailPopup() {
      this.headerTitle = "변경 요청 실패";
      this.content1 = "변경 요청에 실패했습니다.";
      showDialog();
    },
    PWchange() {
      const vm = this;
      const userInfo = JSON.stringify({
        "nickname": this.user.nickname,
        "uid": this.user.id,
        "password": this.user.pw,
        "email": this.user.email,
        "auto_login": this.user.al,
      });
      herokuAPI.changePW(userInfo)
        .then(function (response) {
          console.log("pwChange", response)
          if(response.status == 200) {
            console.log("비번변경 성공")
            localStorage.setItem("UserInfo", userInfo);
            router.push({name: 'mypage'});
          }
        }) 
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 비밀번호 변경 실패");
            vm.changeFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.changeFailPopup();
          }
        });
    }
  }
}
</script>