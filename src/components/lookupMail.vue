<template>
  <v-card>
    <!-- 제목 부분 -->
    <v-card-title class="justify-start">
      {{ mailTitle }}
    </v-card-title>
    
    <v-card-text class="text-end">
      발신자 : {{ mailSender }}
    </v-card-text>
    <v-card-text class="text-end">
      수신자 : {{ mailReceiver }}
    </v-card-text>
    <v-card-text class="text-end">
      작성시간 : {{ sendTime }}
    </v-card-text>

    <!-- 내용 부분 -->
    <v-card-text class="text-center">
      <slot name="body">
        {{ mailContents }}
      </slot>
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center mr-2 pb-4">
      <template>
        <v-btn
          color="#7895B2"
          small
          @click="deletePopup"
        >
          삭제하기
        </v-btn>
      </template>
      <v-btn 
        color="#7895B2"
        small
        @click="$emit('hide')"
      >
        확인
      </v-btn>
    </v-card-actions>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle =titlePopup
        :btn1Title=titleBtn1
        :btn2Title=titleBtn2
        :btn2=btn2
        @hide="hideDialog"
        @submit="checkDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div> {{ content }} </div>
        </template>
      </popup-dialog>
    </v-dialog>
    <!-- 팝업창 형식 -->

  </v-card>
</template>

<script>
import PopupDialog from '@/components/popup.vue';

export default{
  name: "LookupMail",
  components: {
    PopupDialog
  },
  data() {
    return {
      popupDialog: false,
      titlePopup: "",
      titleBtn1: "",
      titleBtn2: "",
      btn2: false,
      content: ""
    };
  },
  props: {
    mailTitle: {
      type: String,
      default: "쪽지 제목",
    },
    mailSender: {
      type: String,
      default: "작성자",
    },
    mailReceiver: {
      type: String,
      default: "수신자",
    },
    sendTime: {
      type: String,
      default: "작성 시간",
    },
    mailContents: {
      type: String,
      default: "내용",
    }
  },
  methods: {
    showDialog(){ // 팝업창 보이기
      this.popupDialog = true
    },
    hideDialog(){ // 팝업창 숨기기
      this.popupDialog = false
    },
    checkDialog(){ // 팝업창 버튼 클릭시
      // 확인 버튼 클릭시 동작 걸기
      // 쪽지 삭제 로직
      this.hideDialog();
    },
    deleteMail(){
      console.log("메일 삭제 로직");
    },
    deletePopup(){
      this.titlePopup = "쪽지 삭제";
      this.content = "쪽지를 삭제하시겠습니까?";
      this.titleBtn1 = "취소";
      this.titleBtn2 = "삭제";
      this.btn2 = true;
      this.showDialog();
    },
  }
};
</script>