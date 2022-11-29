<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="calc(100vh - 120px)" color="#f5efe6">

          <div class="recipe-top d-flex justify-space-between align-center pa-5">
            <span style="color:#7895B2; font-weight:900; font-size:1.3em;">좋아요 누른 사진</span>
          </div>

          <v-row v-if="!isExist" justify="center">
            <v-col cols="12">
              <p style="text-align:center; font-size:1.2em;" class="mt-10">
                좋아요 누른 사진이 없습니다.
              </p>
            </v-col>
          </v-row>

          <v-row justify="center" v-if="isExist">
            <v-col cols="8">
              <v-card height="400" v-for="item in photo" :key="item.post_id" class="my-10" @click="toLookup(item.post_id)">
                <v-row>
                  <v-col class="d-flex justify-space-between">
                    <div class="pl-5">
                      <v-card-title>{{item.nickname}}</v-card-title>
                      <v-card-subtitle>{{item.upload_time}}</v-card-subtitle>
                    </div>
                    <div>
                      <v-icon class="pa-6" large>
                        mdi-thumb-up-outline
                      </v-icon>
                      <span class="pr-6 like-count">{{item.like_count}}</span>
                    </div>
                  </v-col>
                </v-row>

                <div class="mx-6 mt-3">
                  <v-img
                    max-height="250"
                    contain
                    :src="'data:image/jpeg;base64,'+item.photo_link"
                  ></v-img>
                </div>
                
              </v-card>

            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=headerTitle
        :btn1Title=btn1Title
        :btn2=btn2
        @hide="hideDialog"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>{{ content1 }}</div>
        </template>
      </popup-dialog>
    </v-dialog>

  </v-container>
</template>

<style>
.sort-base{
  font-size: 1.2em;
}
.like-count{
  font-size: 1.6em;
}
.write-icon{
  position: fixed;
  bottom: 10%;
  right: 5%;
  z-index: 9;
}
</style>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';
import PopupDialog from '@/components/popup.vue';

export default{
  components: {
    PopupDialog,
  },
  data() {
    return {
    //팝업창
      popupDialog: false,
      headerTitle: "",
      content1: "",
      btn1Title: "확인",
      btn2: false,

    //요리사진 정보들
      photo: [],
      photoID: null,

    //요청한 정보가 있는지 없는지 확인
      isExist : true,
    };
  },
  mounted() {
    let vm = this;
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    herokuAPI.mylikeposts(UserInfo.nickname, 2)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
          console.log("조회 성공");
          for(let i = 0; response.data[i] != null; i++) {
            vm.photo.push(response.data[i]);
          }
          console.log("reponse 길이: " + response.data.length);
          if(response.data.length == 0){
            vm.isExist = false;
          }
        }
      })
      .catch(function (e) {
        if(e.response.status == 405) {
          console.log("405 DB 오류");
          vm.requestFailPopup();
        } else if(e.response.status == 500) {
          console.log("500 Unknown error");
          vm.requestFailPopup();
        }
      });
  },
  methods: {
  // 팝업창 관련
    showDialog() { // 팝업창 보이기
      this.popupDialog = true;
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false;
    },
    requestFailPopup() { // 실패
      this.headerTitle = "요청 실패";
      this.content1 = "사진 게시글 요청에 실패했습니다.";
      this.showDialog();
    },
    sortRequestFailPopup() { // 정렬 실패
      this.headerTitle = "요청 실패";
      this.content1 = "정렬 정보 요청에 실패했습니다.";
      this.showDialog();
    },

  // 클릭한 요리사진 게시글 열람 페이지로 이동
    toLookup(photoID) {
      router.push({
        path: "/mypage/mypagephotolookup/"+photoID,
      })
    },
  }
}
</script>