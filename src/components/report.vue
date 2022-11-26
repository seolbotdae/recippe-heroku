<template>
  <v-card>
    <!-- 제목 부분 -->
    <v-card-title class="justify-start">
      신고하기
    </v-card-title>

    <v-card-text>
      <v-form ref="form" lazy-validation>
        <v-textarea
          label="이곳에 신고 사유를 작성하세요"
          v-model="mailContents"
          required
          outlined
        ></v-textarea>
      </v-form>
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center mr-2 pb-4">
      <v-btn 
        color="#7895B2"
        small
        @click="$emit('hide')"
      >
        취소
      </v-btn>
      <v-btn
        color="#7895B2"
        small
        @click="reportPopup"
      >
        신고하기
      </v-btn>
    </v-card-actions>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=titlePopup
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
import herokuAPI from '@/api/heroku.js';

export default{
  name: "CreateMail",
  components: {
    PopupDialog
  },
  data() {
    return {
      popupDialog: false,
      mailContents: "",
      titlePopup: "",
      content: "",
      titleBtn1: "",
      titleBtn2: "",
      btn2: true,
    };
  },
  props: {
    postType: {
      type: Number
    },
    postID: {
      type: Number
    },
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
      this.reportPost();
      this.hideDialog();
    },
    reportFailPopup(){
      this.titlePopup = "신고 등록 실패";
      this.content = "신고 등록에 실패했습니다.";
      this.titleBtn1 = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    reportPopup(){
      this.titlePopup = "신고 등록";
      this.content = "신고를 등록하시겠습니까?";
      this.titleBtn1 = "취소";
      this.titleBtn2 = "신고하기";
      this.btn2 = true;
      this.showDialog();
    },
    emitMethod(){
      this.$emit('hide');
    },
    reportPost(){ // 신고 등록 로직으로 수정하기
      let vm = this;
      console.log("통합 신고 로직"); // 레시피->1, 댓글->-1, 요리사진->2
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const reportInfo = JSON.stringify ({
        "id": 0,
        "contents": vm.mailContents,
        "post_type": vm.postType,
        "post_id": vm.postID,
        "reporter": UserInfo.nickname
      });
      console.log("신고때 보낼 거", reportInfo);
      if(vm.postType == 1) {
        herokuAPI.recipeReport(reportInfo)
        .then(function (response) {
          if(response.status == 200) {
            console.log("레시피 게시글 신고 성공");
            vm.emitMethod();
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB error");
            vm.reportFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.reportFailPopup();
          }
        });
      } else if(vm.postType == 2) {
        herokuAPI.photoReport(reportInfo)
        .then(function (response) {
          if(response.status == 200) {
            console.log("요리사진 게시글 신고 성공");
            vm.emitMethod();
          }
        })
        .catch(function (e) {
          if(e.response.status == 500) {
            console.log("500 DB error");
            vm.reportFailPopup();
          } else if(e.response.status == 502) {
            console.log("502 Unknown error");
            vm.reportFailPopup();
          }
        });
      } else if(vm.postType == -1) {
        herokuAPI.commentReport(reportInfo)
        .then(function (response) {
          console.log("응답 정보", response);
          if(response.status == 200) {
            console.log("댓글 신고 성공");
            vm.emitMethod();
          }
        })
        .catch(function (e) {
          if(e.response.status == 404) {
            console.log("404 DB error");
            vm.reportFailPopup();
          } else if(e.response.status == 500) {
            console.log("500 Unknown error");
            vm.reportFailPopup();
          }
        });
      }
    },
  }
};
</script>