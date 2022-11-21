<template>
  <v-container>
  
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card height="800" color="#f5efe6">
          <v-btn flat class="ml-5 mt-5"> - 요리 사진 게시판</v-btn>
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
                    <!-- 쪽지 버튼 여기 있음 -->
                    <v-btn icon x-large>
                      <v-icon x-large>mdi-email-arrow-right-outline</v-icon>
                      <div>쪽지</div>
                    </v-btn>
                    
                    <v-card height="20" color="#f5efe6" flat></v-card>
                    <!-- 신고 버튼 여기 있음 -->
                    <v-btn icon x-large>
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
                <v-btn icon x-large>
                  <v-icon x-large>mdi-thumb-up-outline</v-icon>
                  <div>좋아요</div>
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
      isLiked: null
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
            vm.isLiked = response.data.likeInfo;
          }
      })
  },
  methods: {
    onFileChange(e) {
      
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