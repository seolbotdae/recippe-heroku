<template>
  <v-container>
  
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card height="md-800 xl-1000" color="#f5efe6">
          <v-btn text to="/photo" class="ml-5 mt-5"> - 요리 사진 게시판</v-btn>
          <!-- 사용자 정보, 작성일 -->
          
            <v-row>
              <v-col>
                <v-card fill-height color="#f5efe6" class="mt-10" flat>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <v-card-title primary-title style="color:#7895B2">
                          작성자
                        </v-card-title>
                      </v-card>
                    </v-col>
                    <v-col class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 이름 넣어주세요 -->
                        <v-card-title primary-title >
                          {{ requestPhoto.nickname }}
                        </v-card-title>
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="3" class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat style="color:#7895B2">
                        <v-card-title>
                          작성일
                        </v-card-title>
                        
                      </v-card>
                    </v-col>
                    <v-col class="py-0 my-0">
                      <v-card fill-height color="#f5efe6" flat>
                        <!-- 날짜 넣어주세요 -->
                        <v-card-title primary-title>
                          {{ requestPhoto.upload_time }}
                        </v-card-title>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card>
              </v-col>
            </v-row>
            
            <!-- 사진  -->
            <v-row>
              <v-col offset="2" cols="8">
                <v-img 
                lazy-src="https://picsum.photos/id/11/10/6"
                fill-height
                src="https://picsum.photos/id/11/500/300"
                class="mt-10"
                >
                </v-img>
              </v-col>
          
              <v-col cols="2" class="d-flex align-end">
                <v-row justify="left">
                  <div class=".buttons">
                    <!-- 삭제 버튼 여기 있음 -->
                    <v-btn v-if="isMine" icon x-large @click="deletePhoto">
                      <v-icon x-large>mdi-delete-outline</v-icon>
                      <div>삭제</div>
                    </v-btn>
                    
                    <v-card height="20" color="#f5efe6" flat></v-card>
                    <!-- 쪽지 버튼 여기 있음 -->
                    <v-btn v-if="!isMine" icon x-large>
                      <v-icon x-large>mdi-email-arrow-right-outline</v-icon>
                      <div>쪽지</div>
                    </v-btn>
                    
                    <v-card height="20" color="#f5efe6" flat></v-card>
                    <!-- 신고 버튼 여기 있음 -->
                    <v-btn v-if="!isMine" @click="reportPhoto" icon x-large>
                      <v-icon x-large>mdi-alert-octagon</v-icon>
                      <div>신고</div>
                    </v-btn>
                  </div>
                    
                </v-row>
                
                
              </v-col>
            </v-row>

            <v-row justify="center">
              <v-card color="#f5efe6" height="50" flat >
                <!-- 좋아요 버튼 여기 있음 -->
                <v-btn @click="likePhoto" icon x-large>
                  <v-icon x-large>mdi-thumb-up-outline</v-icon>
                  <div v-if="!isLikedAfter">좋아요</div>
                  <div v-if="isLikedAfter">좋아요 취소</div>
                </v-btn>
              </v-card>
            </v-row>

            <!-- 좋아요 수 여기 있음 -->
            <v-row justify="center" class="mt-10 thumbs">
              좋아요 수 {{ requestPhoto.like_count }}
            </v-row>
            
        </v-card>
      </v-col>
    </v-row>
  
  </v-container>
</template>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default{
  data(){
    return{
      requestPhoto: null,
      isLikedBefore: null,
      isLikedAfter: null,
      isMine: null
    }
  },
  mounted() {
    let pid = this.$route.params.id;
    console.log("post_id", pid);
    if(pid == null) {
      console.log("ERROR");
    }
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    let vm = this;
    herokuAPI.photoLookup(pid, UserInfo.nickname)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            vm.requestPhoto = response.data.photoInfo;
            vm.isLikedBefore = response.data.likeInfo;
            vm.isLikedAfter = vm.isLikedBefore;
            if(vm.requestPhoto.nickname == UserInfo.nickname) {
              vm.isMine = true;
            } else {
              vm.isMine = false;
            }
          }
      })
  },
  beforeDestroy() {
    if(this.isLikedBefore != this.isLikedAfter) { // 좋아요 상태 바뀐 경우
      if(this.isLikedBefore) { // 좋아요 취소

      } else { // 좋아요 등록

      }
    }
  },
  methods: {
    deletePhoto() {
      const deleteTarget = {
        "post_id":20,
        "photo_link":"web test",
        "like_count":0,
        "upload_time":"2022-11-22 04:49:01.705849",
        "nickname":"test"
      }
      herokuAPI.photoDelete(deleteTarget) 
        .then(function (response) {
          if(response.status == 200) {
            console.log("응답 정보", response.data);
          }
        })
    },
    likePhoto() {
      this.isLikedAfter = !this.isLikedAfter
      if(this.isLikedAfter) ++requestPhoto.like_count;
      --requestPhoto.like_count;
    },
    // likePhoto() {
    //   let vm = this;
    //   const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    //   let task = ""
    //   if(vm.isLiked) task = "취소"
    //   else task = "등록"
    //   const likeInfo = JSON.stringify({
    //     "like_id": 0,
    //     "nickname": UserInfo.nickname,
    //     "postType": -1,
    //     "postId": vm.requestPhoto.post_id,
    //     "task": task
    //   });
    //   console.log(likeInfo)
    //   if(task == '등록') {
    //     herokuAPI.photoLike(likeInfo)
    //     .then(function (response) {
    //       if(response.status == 200) {
    //         console.log("좋아요 등록 성공");
    //         vm.$router.go();
    //         /* 얘는 그냥 화면 새로고침하는건데 
    //             좋아요를 등록하거나 취소할 때마다 리프레쉬가 필요해서 일단 넣었음
    //             후에 아이콘으로 등록취소를 가르던지 하던 맘대로 바꾸면댐 */
    //       }
    //     })
    //   } else {
    //     herokuAPI.photoUnLike(likeInfo)
    //       .then(function (response) {
    //         if(response.status == 200) {
    //           console.log("좋아요 취소 성공");
    //           vm.$router.go();
    //         }
    //       })
    //   }
    // },
    reportPhoto() {
      let vm = this;
      const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
      const reportInfo = JSON.stringify({
        "id": 0,
        "contents": "web test",
        "post_type": 2,
        "post_id": vm.requestPhoto.post_id,
        "reporter": UserInfo.nickname
      });
      herokuAPI.photoReport(reportInfo)
        .then(function (response) {
          if(response.status == 200) {
            console.log("게시글 신고 성공");
          }
        })
    }
  }
}
</script>

<style>
.back{
  color: aqua;
}

.v-btn__content{
  display: flex;
  flex-direction: column;
}

.thumbs{
  color: rgb(248, 62, 62);
  font-size: 1.7em;
  font-weight: 600;
}

</style>