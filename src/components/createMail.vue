<template>
  <v-card class="overflow-y-auto">
    <!-- 제목 부분 -->
    <v-card-title class="justify-start">
      쪽지 보내기
    </v-card-title>
    
    <v-card-text>
      <v-form ref="form" v-model="valid" lazy-validation>
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
            :rules="receiver_rule"
            outlined
          ></v-text-field>
        </div>
      
        <span>제목</span>
        <div>
          <v-text-field
            label="쪽지의 제목을 작성하세요"
            v-model="mailTitle"
            :rules="title_rule"
            outlined
          ></v-text-field>
        </div>

        <span>내용</span>
        <div>
          <v-textarea
            label="쪽지의 내용을 작성하세요"
            v-model="mailContents"
            :rules="contents_rule"
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
        headerTitle="전송 실패"
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

    <v-snackbar v-model="snackbar" timeout="3000">
      {{ snackbarContents }}
      <template v-slot:action="{ attrs }">
        <v-btn color="blue" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>

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
      valid: true,

      popupDialog: false,
      mailReceiver: "",
      mailTitle: "",
      mailContents: "",

      snackbar: false,
      snackbarContents: "",

    // 유효성 검사
      receiver_rule: [
        v => !!v || '받는 사람의 아이디를 입력하세요.',
        v => !(v && v.length < 6) || '모든 아이디는 6자 이상입니다.',
      ],
      title_rule: [
        v => !!v || '쪽지 제목을 입력하세요.',
      ],
      contents_rule: [
        v => !!v || '쪽지 내용을 입력하세요.',
      ],
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
      const validate = this.$refs.form.validate();
      if(!validate) {
        vm.snackbarContents = "쪽지 정보를 입력해 주세요."
        vm.snackbar = true;
        return;
      }
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