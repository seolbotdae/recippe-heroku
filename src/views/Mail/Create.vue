<template>
  <v-container>
      쪽지 작성 화면
    <v-btn @click="sendMail" style="width: 100%">쪽지 보내기</v-btn>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';

export default{
  data(){
    return {
      sendedMail: null,
    }
  },
  methods: {
    sendMail() {
      let vm = this;
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const newMail = JSON.stringify (
        {
          "mail_id" : 0,
          "nickname" : UserInfo.nickname,
          "receiver" : "bye",
          "title" : "web test",
          "contents" : "web test",
          "send_time" : "",
          "sender_check" : 0,
          "receiver_check" : 0
        }
      );
      herokuAPI.mailSend(newMail) 
        .then(function (response) {
          console.log("전송 정보",  newMail);
          if(response.status == 200) {
            console.log("응답 정보", response.data);
          }
        })
    }
  }
}

</script>