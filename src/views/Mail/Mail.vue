<template>
  <v-container>
    쪽지함 화면
    <v-btn @click="toLookup" style="width: 100%">쪽지 Lookup 이동</v-btn>
    <v-btn @click="toCreate" style="width: 100%">쪽지 Create 이동</v-btn>
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default {
  data () {
    return {
      mails: [],
      mailID: null,
      total_page: null,
    }
  },
  mounted() {
    let vm = this;
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    herokuAPI.mailList(UserInfo.nickname, 1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data.mailList[i] != null; i++) {
              vm.mails.push(response.data.mailList[i]);
            }
            vm.total_page = response.data.total_page;
          }
      })
  },
  methods: {
    toLookup() {
      router.push({
        path: "/mail/lookup/",
      })
    },
    toCreate() {
      router.push({
        path: "/mail/create/",
      })
    },
  }
}
</script>