<template>
  <v-container>
    쪽지함 화면
    <v-btn @click="toLookup" style="width: 100%">쪽지 Lookup 이동</v-btn>
    <v-btn @click="toCreate" style="width: 100%">쪽지 Create 이동</v-btn>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="LookupMail"
    >
      <popup-dialog
        :headerTitle=1
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
import LookupMail from '@/components/lookupMail.vue';

export default{
  components: {
    LookupMail
  },
  data () {
    return {
      LookupMail: false,
      mails: [],
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
    showMail(){ // 팝업창 보이기
      this.popupDialog = true
    },
    hideMail(){ // 팝업창 숨기기
      this.popupDialog = false
    },
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