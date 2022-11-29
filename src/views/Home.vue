<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="400" color="#f5efe6" class="pa-3">
          <v-card-title class="my-text recommend-recipe-title pa-5">
            추천 레시피
          </v-card-title>

          <!-- 추천 레시피 v-card -->
          <v-card height="100" class="mx-5 mb-5" v-for="item in recipes" :key="item.title" color="#E8DFCA" @click="toLookup(item.post_id)">
            <div class="d-flex align-center">
              <!-- 음식을 받아와서 넣으시면 됩니다. -->
              <span class="mx-10 py-3" style="font-size:1.1em; font-weight:600; color:#7895B2">{{item.title}}</span>
              <v-icon color="red" v-if="item%5+1>=1">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=2">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=3">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=4">mdi-chili-mild</v-icon>
              <v-icon color="red" v-if="item%5+1>=5">mdi-chili-mild</v-icon>
            </div>
            <div style="border: 0.5px solid #7895B2;" class="mx-5"></div>
            <div class="d-flex align-center justify-space-between">
              <div style="color:#7895B2" class="ml-10 py-3">
                <!-- 날짜를 받아와서 넣으시면 됩니다. -->
                <span class="mr-3">{{item.upload_time}}</span>
                <!-- 이름을 받아와서 넣으시면 됩니다 -->
                <span>{{item.title}}</span>
              </div>
              <div class="mr-6">
                <!-- 좋아요 받아와서 넣으시면 됩ㄴ디ㅏ. -->
                <v-icon color="red">mdi-thumb-up-outline</v-icon> {{item.like_count}}
                <!-- 댓글 가져와서 넣으시면 됩니다. -->
                <v-icon color="blue" class="ml-2">mdi-comment-processing-outline</v-icon> {{item.comment_count}}
                <!-- 조회수 가져와서 넣으시면 됩니다. -->
                <v-icon color="green" class="ml-2">mdi-eye-outline</v-icon> {{item.views}}
              </div>
            </div>
          </v-card>

        </v-card>

        <v-card min-height="200" color="#f5efe6" class="pa-3 mt-3 overflow-auto">
          <v-card-title class="my-text recommend-recipe-title pa-5">
            추천 요리 사진
          </v-card-title>
          
          <!-- 추천 요리 사진 v-for 입니다. -->
          <div class="d-flex align-center photo-box">
            <div v-for="item in photo" :key="item.photo_link" @click="toLookupPhoto(item.post_id)">
              <v-img
                contain
                max-width="300"
                :src="'data:image/jpeg;base64,'+item.photo_link"
                class="mx-4"
              ></v-img>
            </div>
          </div>
          

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.my-text{
  color: #42688e;
}

.recommend-recipe-title{
  color: #7ca5c9;
  font-weight: 900;
}

.photo-box{
  cursor: pointer;
}
</style>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';

export default{
  data() {
    return {
    //요리사진 정보들
      photo: [],
      photoID: null,

    //레시피 정보들
      recipes: [],
      recipeID: null,
      total_page: null,

    //페이지네이션 길이
      pageLength : 1,
    };
  },
  mounted() {
  let vm = this;
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            vm.pageLength = response.data.total_page;
            for(let i = 0; i < 5; i++) {
              vm.recipes.push(response.data.recipeList[i]);
            }
          }
      })
      .catch(function (e) {
        if(e.response.status == 500) {
          console.log("500 DB 오류");
        } else if(e.response.status == 502) {
          console.log("502 Unknown error");
        }
      });

      herokuAPI.photoList(1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
          console.log("조회 성공");
          vm.pageLength = response.data.total_page;
          console.log(vm.pageLength);
          for(let a = 0; a < 5; a++) {
            vm.photo.push(response.data.photoList[a]);
          }
          console.log(vm.photo);
        }
      })
      .catch(function (e) {
        if(e.response.status == 500) {
          console.log("500 DB 오류");
        } else if(e.response.status == 502) {
          console.log("502 Unknown error");
        }
      });
  },
  methods: {
    toLookup(recipeID) {
      router.push({
        path: "/recipe/lookup/"+recipeID,
      })
    },
    // 클릭한 요리사진 게시글 열람 페이지로 이동
    toLookupPhoto(photoID) {
      router.push({
        path: "/photo/lookup/"+photoID,
      })
    },
  }
}

</script>