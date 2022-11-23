<template>
  <v-container>

    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" color="#f5efe6" class="pa-4">
          <div class="mailbox-title px-16 py-10">
            쪽지함
          </div>

          <!-- 불러오는 메일 v-for 입니다. -->
          <v-card min-height="100" color="#fefefe" class="my-5 mx-16" v-for="item in mails" :key="item">
            <v-card-title primary-title class="mb-0">
              {{item.title}}
            </v-card-title>
            
            <div class="d-flex align-top justify-space-between mx-4" >
              <span>보낸사람:{{item.nickname}}</span>
              <span>받는사람:{{item.receiver}}</span>
              <span>{{item.send_time}}</span>
            </div>
            
            
          </v-card>
        </v-card>

        <!-- 쪽지 추가 버튼 -->
        <v-btn fab x-large color="#E8DFCA" class="write-btn">
          <v-icon color="#7895B2">mdi-plus</v-icon>
        </v-btn>

      </v-col>
    </v-row>

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

<style>

.mailbox-title{
  font-size: 2.3em;
}

.my-text{
  color:#7895B2;
}

.write-btn{
  position: fixed;
  bottom: 10%;
  right: 5%;
}

</style>

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
    toCreate() {
      router.push({
        path: "/mail/create/",
      })
    },
  }
}
</script>