<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" color="#f5efe6">

          <v-row justify="center">
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

                <v-row justify="center">
                  <v-col cols="8">
                    <v-img
                      lazy-src="https://w.namu.la/s/45e2317ae59261dcc8643bfa26897a253a3162b145e770687fcf649e461a99ae3b87401baf461913986519a8ed951db7d5f477222a5fe09d8d0b1c6c988e33c97e4d25588755b598af2025a04d3a3fc4b0c149cc3fdfa702f71ae970575d19ef"
                      contain
                      src="https://w.namu.la/s/45e2317ae59261dcc8643bfa26897a253a3162b145e770687fcf649e461a99ae3b87401baf461913986519a8ed951db7d5f477222a5fe09d8d0b1c6c988e33c97e4d25588755b598af2025a04d3a3fc4b0c149cc3fdfa702f71ae970575d19ef"
                    ></v-img>
                  </v-col>
                </v-row>
                
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