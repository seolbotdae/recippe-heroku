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
                <v-col xl12 md10 cols="4">
                  <v-card color="#fefefe" height="400" rounded="xl">
                    <v-card-title id="title" class="pa-10 justify-center fontsize">비밀번호 변경</v-card-title>

                    <v-col>
                      <v-text-field filled label="새 비밀번호" placeholder="새로운 비밀번호 입력."></v-text-field>
                      <v-text-field filled label="비밀번호 확인" placeholder="비밀번호 확인."></v-text-field>
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
    PWchange() {
      console.log("change pw methods");
    }
  }
}
</script>