<template>
  <v-container>
    <v-layout>
      <!-- 바깥쪽 살구색 배경 -->
      <v-row justify="center">
        <v-col cols="8"> 
          <v-card color="#f5efe6" height="800">
            <v-card color='#f5efe6' height="100" flat></v-card>
            <!-- 안쪽 하얀 배경 -->
            <v-row justify="center">
              <v-col cols="md-6 xl-4" align-content="center">
                <v-card color='#fefefe' height="600" rounded="xl">
          
                  <v-card-title class="justify-center">닉네임 변경</v-card-title>
                  <v-card-title class="pl-15">현재 닉네임</v-card-title>

                  <v-card-title class="justify-center pb-15">{{ nickname }}</v-card-title>
                  <v-card-title class="pt-15 pl-15">새로운 닉네임</v-card-title>
                  
                  <v-col offset="2" cols="8">
                    <v-form ref="form" v-model="valid" lazy-validation>
                      <v-text-field 
                        filled 
                        v-model="user.nickname" 
                        label="새 닉네임" 
                        :rules="nn_rule" 
                        placeholder="새로운 닉네임 입력." 
                        class="pb-10"
                      ></v-text-field>
                    </v-form>
                  </v-col>

                  <v-row justify="center">
                    
                    <v-card-actions>
                      <v-btn outlined width="120" to="/mypage">취소</v-btn>
                    </v-card-actions>

                    <v-card-actions>
                      <v-btn outlined width="120" @click="NNchange()">확인</v-btn>
                    </v-card-actions>
                  
                  </v-row>

                </v-card>
              </v-col>
            </v-row>

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
          <div v-if="content2 != ''"> {{ content2 }} </div>
        </template>
      </popup-dialog>
    </v-dialog>

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
      valid: true,

      popupDialog: false,
      headerTitle: "",
      content1: "",
      content2: "",
      
      user: {
        email: '',
        id: '',
        nickname: '',
        pw: '',
        pwcheck: '',
        al: ''
      },
      nickname: '',
      
    // 유효성 검사
      nn_rule: [
        v => !!v || '새로운 닉네임을 입력하세요.',
      ],
    };
  },
  created() {
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    this.nickname = UserInfo.nickname
    this.user.id = UserInfo.uid
    this.user.pw = UserInfo.password
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
      this.headerTitle = "서버 오류";
      this.content1 = "닉네임 변경에 실패했습니다.";
      this.content2 = "재시도 해주십시오.";
      this.showDialog();
    },
    sameNickPopup() {
      this.headerTitle = "닉네임 중복";
      this.content1 = "중복된 닉네임입니다.";
      this.content2 = "";
      this.showDialog();
    },
    NNchange() {
      let vm = this;
      const validate = this.$refs.form.validate();
      if(!validate) {
        vm.headerTitle = "입력";
        vm.content1 = "새로운 닉네임을 입력해주세요.";
        vm.showDialog();
        return;
      }
      const userInfo = JSON.stringify({
        "nickname": this.user.nickname,
        "uid": this.user.id,
        "password": this.user.pw,
        "email": this.user.email,
        "auto_login": this.user.al,
      });
      herokuAPI.changeNN(userInfo)
        .then(function (response) {
          console.log("nnChange", response)
          if(response.status == 200) {
            console.log("닉넴변경 성공")
            localStorage.setItem("UserInfo", userInfo);
            router.push({name: 'mypage'});
          }
        }) 
        .catch(function (e) {
          if(e.response.status == 400) {
            console.log("400 닉네임 중복 error");
            vm.sameNickPopup();
          } else if(e.response.status == 500) {
            console.log("500 닉네임 변경 실패 or DB오류");
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