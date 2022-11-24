<template>
  <v-container>
    쪽지 화면
    <v-btn @click="deleteMail" style="width: 100%">쪽지 삭제하기</v-btn>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default {
  data () {
    return {
      requestMail: null
    }
  },
  mounted() {
    let vm = this;
    herokuAPI.mailLookup(1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            vm.requestMail = response.data;
          }
      })
  },
  methods: {
    deleteMail() {
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const deleteTarget = JSON.stringify (
        {
          "mail_id" : 40,
          "nickname" : UserInfo.nickname,
          "receiver" : "bye",
          "title" : "web test",
          "contents" : "web test",
          "send_time" : "",
          "sender_check" : 0,
          "receiver_check" : 0
        }
      );
      herokuAPI.mailDelete(deleteTarget) 
        .then(function (response) {
          console.log("전송 정보",  deleteTarget);
          if(response.status == 200) {
            console.log("응답 정보", response.data);
          }
        })
    }
  }
}
</script>