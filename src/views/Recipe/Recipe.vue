<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <!-- 요리 직접 검색과 카테고리 선택 -->
        <v-card min-height="100" color="#f5efe6" class="mb-3">
          <!-- 요리 검색 윗줄 -->
          <div class="find-cook flex align-end mb-2" v-if="!categoryBoolean">
            <dropdown class="my-dropdown-toggle my-0 ml-5"
              :options="search_standard" 
              :selected="search_object" 
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'검색 기준'"
              :closeOnOutsideClick="boolean">
            </dropdown>
            <v-text-field
              label="요리를 검색하세요"
              hide-details="auto"
              class="mx-5"
            ></v-text-field>
            <v-btn class="mx-3" color="#E8DFCA">
              검색
            </v-btn>
          </div>
          <div class="black-line mx-3" v-if="!categoryBoolean"></div>
          <!-- 요리 검색 밑줄 -->
          <div class="category-search-dropdown mt-2 flex-column">
            <v-btn color="#f5efe6" depressed @click="methodToChangeCategoryBoolean" v-if=!categoryBoolean>카테고리 검색</v-btn>
            <v-btn color="#f5efe6" depressed @click="methodToChangeCategoryBoolean" v-if=categoryBoolean>키워드 검색</v-btn>
            <!-- 카테고리 슬라이드 -->
            <v-card fill-height color="#E8DFCA" v-if=categoryBoolean>
              <v-card min-height="100" class="my-5 mx-5">
                <v-card-title primary-title class="my-text ml-5">
                  재료
                </v-card-title>
                <v-radio-group v-model="value" row class="mt-0 ml-10">
                  <v-radio label="육류" value="육류"></v-radio>
                  <v-radio label="어류" value="어류"></v-radio>
                  <v-radio label="채소류" value="채소류"></v-radio>
                  <v-radio label="과일류" value="과일류"></v-radio>
                </v-radio-group>
              </v-card>

              <v-card min-height="100" class="my-5 mx-5">
                <v-card-title primary-title class="my-text ml-5">
                  조리법
                </v-card-title>
                <v-radio-group v-model="value" row class="mt-0 ml-10">
                  <v-radio label="구이" value="구이"></v-radio>
                  <v-radio label="볶음" value="볶음"></v-radio>
                  <v-radio label="조림" value="조림"></v-radio>
                  <v-radio label="튀김" value="튀김"></v-radio>
                </v-radio-group>
              </v-card>

              <v-card min-height="100" class="my-5 mx-5">
                <v-card-title primary-title class="my-text ml-5">
                  매운맛 단계
                </v-card-title>
                <v-radio-group v-model="value" row class="mt-0 ml-10">
                  <v-radio label="1단계" value="1단계"></v-radio>
                  <v-radio label="2단계" value="2단계"></v-radio>
                  <v-radio label="3단계" value="3단계"></v-radio>
                  <v-radio label="4단계" value="4단계"></v-radio>
                  <v-radio label="5단계" value="5단계"></v-radio>
                </v-radio-group>
              </v-card>
              <div class="d-flex justify-end ma-5">
                <v-btn color="#7895B2">검색</v-btn>
              </div>
            </v-card>
          </div>
        </v-card>

        <v-card min-height="1000" color="#f5efe6">
          <!-- 상단 레시피 게시판 글씨랑 정렬기준 드롭다운 -->
          <div class="recipe-top d-flex justify-space-between align-center pa-5">
            <span style="color:#7895B2; font-weight:900; font-size:1.3em;">레시피 게시판</span>
            <!-- 드롭다운으로 대체할 예정 -->
            <dropdown class="my-dropdown-toggle"
              :options="arrayOfObjects" 
              :selected="object" 
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'정렬 기준'"
              :closeOnOutsideClick="boolean">
            </dropdown>
          </div>

          <!-- 글쓰기 버튼 -->
          <v-btn fab to="/recipe/create" x-large color="primary" class="write-icon">
            <v-icon dark>mdi-pencil-outline</v-icon>
          </v-btn>

          <!-- 임시버늩 -->
          <v-btn fab x-large color="primary" to="/recipe/edit" class="write-icon">
            <v-icon dark>mdi-pencil-outline</v-icon>
          </v-btn>

          <!-- 음식 v card -->
          <v-card height="100" class="mx-5 mb-5" v-for="item in 20">
            <div class="d-flex align-center">
              <!-- 음식을 받아와서 넣으시면 됩니다. -->
              <span class="mx-10 py-3" style="font-size:1.1em; font-weight:600; color:#7895B2">김치볶음밥</span>
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
                <span class="mr-3">2022/06/07</span>
                <!-- 이름을 받아와서 넣으시면 됩니다 -->
                <span>홍길동</span>
              </div>
              <div class="mr-6">
                <!-- 좋아요 받아와서 넣으시면 됩ㄴ디ㅏ. -->
                <v-icon color="red">mdi-thumb-up-outline</v-icon> 1.1K
                <!-- 댓글 가져와서 넣으시면 됩니다. -->
                <v-icon color="blue" class="ml-2">mdi-comment-processing-outline</v-icon> 5m
                <!-- 조회수 가져와서 넣으시면 됩니다. -->
                <v-icon color="green" class="ml-2">mdi-eye-outline</v-icon> 1.5K
              </div>
            </div>
          </v-card>



          <!-- 페이지 이동 -->
          <v-pagination v-model="page" length="5" class="pb-10">
          </v-pagination>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.find-cook{
  display: flex;
}

.black-line{
  border: 0.4px solid #7895B2;
}

.category-search-dropdown{
  display: flex;
  justify-content: center;
}

.write-icon{
  position: fixed;
  bottom: 10%;
  right: 5%;
}

.my-text{
  color:#7895B2;
}

</style>


<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';
import dropdown from 'vue-dropdowns';

export default {
  data () {
    return {
      headers: [
        { text: 'id', value: 'post_id' },
        { text: 'title', value: 'title' },
        { text: 'nickname', value: 'nickname' },
        { text: 'spicy', value: 'degree_of_spicy' },
        { text: 'like', value: 'like_count' },
        { text: 'comment', value: 'comment_count' },
        { text: 'view', value: 'views' },
        { text: 'time', value: 'upload_time' },
      ],
      recipes: [],
      recipeID: null,
      total_page: null,
      //검색 기준
      search_standard: [
          {name: '요리 이름'},
          {name: '작성자'}
      ],
      search_object: {
        name: '검색 기준',
      },
      //정렬 기준 objects
      arrayOfObjects: [
        { name: '최근 순'},
        { name: '조회 순'},
        { name: '좋아요 순'}
      ],
      object: {
        name: '정렬 기준',
      },
      //맵기 단계
      hotGrade: 2,
      //카테고리 슬라이드
      categoryBoolean : false,
    }
  },
  components: {
    'dropdown': dropdown,
  },
  mounted() {
    let vm = this;
    herokuAPI.recipeList(1)
      .then(function(response) {
        console.log("리스트 응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data.recipeList[i] != null; i++) {
              vm.recipes.push(response.data.recipeList[i]);
            }
          }
      })
  },
  methods: {
    toLookup(recipeID) {
      router.push({
        path: "/recipe/lookup/"+recipeID,
      })
    },
    searchRecipeList() {
      let list = [];
      let tp;
      const searchInfo = JSON.stringify({
        "searchType": "카테고리",
        "categories": "test0-test2",
        "keywordType": null,
        "keyword": null,
        "page": 1
      });
      herokuAPI.recipeSearch(searchInfo)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
              console.log("검색 성공");
              for(let i = 0; response.data.recipeList[i] != null; i++) {
                list.push(response.data.recipeList[i]);
              }
              tp = response.data.total_page;
            }
        })
      this.recipes = list;
      this.total_page = tp;
    },
    sortRecipeList() {
      let list = [];
      const sortInfo = JSON.stringify({
        "arrangeBy": "좋아요 순",
        "page": 1
      });
      herokuAPI.recipeSort(sortInfo)
        .then(function (response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("정렬 성공");
            for(let i = 0; response.data[i] != null; i++) {
              list.push(response.data[i]);
            }
          }
        })
      this.recipes = list;
    },
    methodToRunOnSelect(payload) {
      this.object = payload;
    },
    // 카테고리 검색 슬라이드 버튼 함수
    methodToChangeCategoryBoolean() {
      if (this.categoryBoolean == true) {
        this.categoryBoolean = false
      }else{
        this.categoryBoolean = true
      }

    }
  }
}
</script>