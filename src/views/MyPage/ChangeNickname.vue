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
              <v-col xl12 md10 cols="4" align-content="center">
                <v-card color='#fefefe' height="600" rounded="xl">
          
                  <v-card-title class="justify-center">닉네임 변경</v-card-title>
                  <v-card-title class="pl-15">현재 닉네임</v-card-title>

                  <v-card-title class="justify-center pb-15">{{ nickname }}</v-card-title>
                  <v-card-title class="pt-15 pl-15">새로운 닉네임</v-card-title>
                  
                  <v-col offset="2" cols="8">
                    <v-text-field filled v-model="user.nickname" label="새 닉네임" placeholder="새로운 닉네임 입력." class="pb-10"></v-text-field>
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
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default {
  data() {
    return {
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
    this.user.pw = UserInfo.password
    this.user.email = UserInfo.email
    this.user.al = UserInfo.auto_login
  },
  methods: {
    NNchange() {
      const userInfo = JSON.stringify({
        "nickname": this.user.nickname,
        "uid": this.user.id,
        "password": this.user.pw,
        "email": this.user.email,
        "auto_login": false,
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
          console.log(e);
        });
    }
  }
}
</script>