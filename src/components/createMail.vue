<template>
  <v-card class="overflow-y-auto">
    <!-- 제목 부분 -->
    <v-card-title class="justify-start">
      쪽지 보내기
    </v-card-title>
    
    <v-card-text>
      <v-form>
        <span>받는 사람</span>
        <div>
          <v-text-field
            v-if="receiverFixed"
            v-model="mailReceiver"
            disabled
            outlined
          ></v-text-field>
          <v-text-field
            v-else
            label="받을 사람의 닉네임을 작성하세요"
            v-model="mailReceiver"
            outlined
          ></v-text-field>
        </div>
      
        <span>제목</span>
        <div>
          <v-text-field
            label="쪽지의 제목을 작성하세요"
            v-model="mailTitle"
            outlined
          ></v-text-field>
        </div>

        <span>내용</span>
        <div>
          <v-textarea
            label="쪽지의 내용을 작성하세요"
            v-model="mailContents"
            outlined
          ></v-textarea>
        </div>
      </v-form>
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center mr-2 pb-4">
      <v-btn 
        color="#7895B2"
        small
        @click="$emit('hide')"
      >
        뒤로가기
      </v-btn>
      <v-btn
        color="#7895B2"
        small
        @click="sendMail"
      >
        보내기
      </v-btn>
    </v-card-actions>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        headerTitle="쪽지 등록 실패"
        btn1Title="확인"
        :btn2=false
        @hide="hideDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div> 쪽지 전송에 실패했습니다. </div>
        </template>
      </popup-dialog>
    </v-dialog>

  </v-card>
</template>

<script>
import PopupDialog from '@/components/popup.vue';
import herokuAPI from '@/api/heroku.js';

export default{
  name: "CreateMail",
  components: {
    PopupDialog
  },
  data() {
    return {
      popupDialog: false,
      mailReceiver: "",
      mailTitle: "",
      mailContents: ""
    };
  },
  props: {
    receiverFixed: {
      type: Boolean,
      default: false,
    },
    receiver: {
      type: String,
      default: "",
    },
  },
  mounted(){
    this.mailReceiver = this.receiver;
  },
  methods: {
    showDialog(){ // 팝업창 보이기
      this.popupDialog = true
    },
    hideDialog(){ // 팝업창 숨기기
      this.popupDialog = false
    },
    emitMethod(){
      if(this.receiverFixed == false) this.$emit('update');
      this.$emit('hide');
    },
    sendMail(){ 
      let vm = this;
      console.log("메일 등록 로직");
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const sendMail = JSON.stringify (
        {
          "mail_id" : null,
          "nickname" : UserInfo.nickname,
          "receiver" : vm.mailReceiver,
          "title" : vm.mailTitle,
          "contents" : vm.mailContents,
          "send_time" : "",
          "sender_check" : 0,
          "receiver_check" : 0
        }
      );
      herokuAPI.mailSend(sendMail) 
        .then(function (response) {
          console.log("response", response);
          if(response.status == 200) {
            console.log("성공 응답", response.data);
            vm.emitMethod();
          }
        })
        .catch(function (e) {
          if(e.response.status == 404) {
            console.log("404 error");
            vm.showDialog();
          } else if(e.response.status == 500) {
            console.log("500 Unknown error");
            vm.showDialog();
          }
        });
    },
  }
};
</script>