<template>
  <v-container>

    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" color="#f5efe6" class="pa-4">
          <div class="mailbox-title px-16 py-10">
            쪽지함
          </div>

          <!-- 불러오는 메일 v-for 입니다. -->
          <v-card min-height="100" color="#fefefe" class="my-5 mx-16" @click="showMailLookup(index)" v-for="(val,index) in mails" :key="val.mail_id">
            <v-card-title primary-title class="mb-0">
              {{val.title}}
            </v-card-title>
            
            <div class="d-flex align-top justify-space-between mx-4" >
              <span>보낸사람:{{val.nickname}}</span>
              <span>받는사람:{{val.receiver}}</span>
              <span>{{val.send_time.split(/[T]/)[0]}}</span>
            </div>

          </v-card>
        </v-card>

        <!-- 쪽지 추가 버튼 -->
        <v-btn fab x-large color="#E8DFCA" class="write-btn" @click="showMailCreate()">
          <v-icon color="#7895B2">mdi-plus</v-icon>
        </v-btn>

      </v-col>
    </v-row>

    <!-- 쪽지 열람 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="lookupMailDialog"
    >
      <lookup-mail-dialog
        :mailTitle=openMail.title
        :mailID=openMail.mail_id
        :mailSender=openMail.nickname
        :mailReceiver=openMail.receiver
        :sendTime=openMail.send_time
        :mailContents=openMail.contents
        btn1Title="확인"
        :btn2=false
        @hide="hideMailLookup"
        @update="updateList"
      />
    </v-dialog>

    <!-- 쪽지 작성 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="createMailDialog"
    >
      <create-mail-dialog
        @hide="hideMailCreate"
        @update="updateList"
      />
    </v-dialog>

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
import LookupMailDialog from '@/components/lookupMail.vue';
import CreateMailDialog from '@/components/createMail.vue';

export default{
  components: {
    LookupMailDialog,
    CreateMailDialog
  },
  data () {
    return {
      lookupMailDialog: false,
      createMailDialog: false,
      mails: [],
      openMail: {},
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
    showMailLookup(index){ // 팝업창 보이기
      this.openMail = this.mails[index];
      this.lookupMailDialog = true;
    },
    hideMailLookup(){ // 팝업창 숨기기
      this.lookupMailDialog = false;
    },
    showMailCreate(){ // 팝업창 보이기
      this.createMailDialog = true;
    },
    hideMailCreate(){ // 팝업창 숨기기
      this.createMailDialog = false;
    },
    updateList(){ // 쪽지 목록 업데이트
      this.$router.go();
    },
  }
}
</script>