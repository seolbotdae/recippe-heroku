<template>
  <v-container>
    <v-row justify="center">
      <v-col class="col-xl-8 col-md-10">
        <v-card min-height="800" color="#f5efe6">

          <!-- 정렬 기준 -->
          <v-row>
            <v-col offset="9">
              <dropdown class="my-dropdown-toggle my-5 "
              :options="search_standard" 
              :selected= currentSearchOption
              v-on:updateOption="methodToRunOnSelect" 
              :placeholder="'검색 기준'"
              :closeOnOutsideClick="true">
            </dropdown>
            </v-col>
          </v-row>

          <v-row justify="center">
            <v-col cols="8">
              <v-card height="400" v-for="item in photo" :key="item" class="my-10" @click="toLookup(item.post_id)">
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

              <!-- 페이지 이동 -->
              <v-pagination 
                v-model="page"
                :length="pageLength"
                class="pb-10"
                @input="handlePage"
              >
              </v-pagination>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style>
.sort-base{
  font-size: 1.2em;
}
.like-count{
  font-size: 1.6em;
}
</style>

<script>
import herokuAPI from '@/api/heroku.js';
import router from '@/router/index.js';
import dropdown from 'vue-dropdowns';

export default {
  data() {
    return {
      photo: [],
      photoID: null,
      search_standard: [
          {name: '최근 순'},
          {name: '좋아요 순'}
      ],

      currentSearchOption : {
        name: "최근 순"
      },

      search_object: {
        name: "정렬 기준",
      },
      page: 1,
      pageLength: null,
    };
  },
  mounted() {
    let vm = this;
    
    herokuAPI.photoList(1)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
          console.log("조회 성공");
          vm.pageLength = response.data.total_page;
          console.log(vm.pageLength);

          for(let i = 0; response.data.photoList[i] != null; i++) {
            vm.photo.push(response.data.photoList[i]);
          }
        }
      })

    
  },

  components: {
    'dropdown': dropdown,
  },

  methods: {
    toLookup(photoID) {
      router.push({
        path: "/photo/lookup/"+photoID,
      })
    },

    //사진 리스트를 정렬해서 즉시 변경하는 함수
    sortPhotoList(page, order_by) {
      let vm = this;
      vm.photo = [];

      const sortInfo = JSON.stringify({
        "arrangeBy": order_by,
        "page": page
      });

      herokuAPI.photoSort(sortInfo)
        .then(function (response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("정렬 성공");
            for(let i = 0; response.data.photoList[i] != null; i++) {
              vm.photo.push(response.data.photoList[i]);
            }
            console("리스트 내용 : ", vm.photo);
            window.scrollTo({top:0});
          }
        })
    },
    //정렬 드롭다운 선택시 실행되는 함수
    methodToRunOnSelect(payload) {
      this.object = payload;
      if (this.object.name == "최근 순"){
        console.log("최근 순 선택");
        this.currentSearchOption.name = "최근 순";
        this.page=1;

        this.sortPhotoList(this.page, this.currentSearchOption.name);
      }else if(this.object.name == "좋아요 순"){
        console.log("좋아요 순 선택");
        this.currentSearchOption.name = "좋아요 순";
        this.page=1;
        this.sortPhotoList(this.page, this.currentSearchOption.name);
      }
    },

    handlePage(){
      let vm = this;

      if(this.currentSearchOption.name == "최근 순"){
        this.sortPhotoList(vm.page, this.currentSearchOption.name);
      }else if(this.currentSearchOption.name == "좋아요 순"){
        this.sortPhotoList(vm.page, this.currentSearchOption.name);
      }
    },
  }
}
</script>