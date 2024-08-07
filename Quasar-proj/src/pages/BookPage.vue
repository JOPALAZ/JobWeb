<template>
  <q-page class="q-pa-md">
    <!-- Block for Books -->
    <q-card>
      <q-card-section>
        <div class="text-h6">Books</div>
      </q-card-section>

      <q-card-section>
        <q-table
          :rows="books"
          :columns="bookColumns"
          row-key="id"
          virtual-scroll
          :rows-per-page-options="[0]"
        >
          <template v-slot:top-right>
            <q-btn color="primary" @click="openAddBookDialog">Add Book</q-btn>
          </template>

          <template v-slot:body-cell-edit="props">
            <q-td :props="props">
              <q-btn
                color="secondary"
                icon="edit"
                @click="editBook(props.row)"
              />
            </q-td>
          </template>
          
          <template v-slot:body-cell-delete="props">
            <q-td :props="props">
              <q-btn
                color="negative"
                icon="delete"
                @click="deleteBook(props.row.id)"
              />
            </q-td>
          </template>
        </q-table>
        <div class="row justify-end q-mt-md">
          <q-select
            v-model="paginationBooks.rowsPerPage"
            :options="[5, 10, 15, 20]"
            dense
            outlined
            style="min-width: 220px;"
          />
          <q-btn 
            :disable="paginationBooks.page === 1" 
            @click="changeBookPage(paginationBooks.page - 1)">Previous</q-btn>
          <q-btn 
            :disable="paginationBooks.page * paginationBooks.rowsPerPage >= paginationBooks.rowsNumber" 
            @click="changeBookPage(paginationBooks.page + 1)">Next</q-btn>
        </div>
      </q-card-section>
    </q-card>

    <!-- Block for Authors -->
    <q-card class="q-mt-md">
      <q-card-section>
        <div class="text-h6">Authors</div>
      </q-card-section>

      <q-card-section>
        <q-table
          :rows="authors"
          :columns="authorColumns"
          row-key="id"
          virtual-scroll
          :rows-per-page-options="[0]"
        >
          <template v-slot:top-right>
            <q-btn color="primary" @click="openAddAuthorDialog">Add Author</q-btn>
          </template>
          
          <template v-slot:body-cell-edit="props">
            <q-td :props="props">
              <q-btn
                color="secondary"
                icon="edit"
                @click="editAuthor(props.row)"
              />
            </q-td>
          </template>
          
          <template v-slot:body-cell-delete="props">
            <q-td :props="props">
              <q-btn
                color="negative"
                icon="delete"
                @click="deleteAuthor(props.row.id)"
              />
            </q-td>
          </template>
        </q-table>
        <div class="row justify-end q-mt-md">
          <q-select
            v-model="paginationAuthors.rowsPerPage"
            :options="[5, 10, 15, 20]"
            dense
            outlined
            style="min-width: 220px;"
          />
          <q-btn 
            :disable="paginationAuthors.page === 1" 
            @click="changeAuthorPage(paginationAuthors.page - 1)">Previous</q-btn>
          <q-btn 
            :disable="paginationAuthors.page * paginationAuthors.rowsPerPage >= paginationAuthors.rowsNumber" 
            @click="changeAuthorPage(paginationAuthors.page + 1)">Next</q-btn>
        </div>
      </q-card-section>
    </q-card>

    <!-- Add Book Dialog -->
    <q-dialog v-model="addBookDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Add New Book</div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="newBook.title" label="Book Title" outlined />
          <q-select
            v-model="newBook.authors"
            :options="authorsOptions"
            label="Author"
            outlined
            multiple
            emit-value
            map-options
            style="max-width: 220px;"
          />
          <q-input v-model="newBook.publish_date" label="Publication Date" type="date" outlined />
          <q-input v-model="newBook.isbn" label="ISBN" outlined />
        </q-card-section>

        <q-card-actions>
          <q-btn color="primary" @click="addBook">Add</q-btn>
          <q-btn @click="addBookDialog = false">Close</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Edit Book Dialog -->
    <q-dialog v-model="editBookDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Edit Book</div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="currentBook.title" label="Book Title" outlined />
          <q-select
            v-model="currentBook.authors"
            :options="authorsOptions"
            label="Author"
            outlined
            multiple
            emit-value
            map-options
            style="max-width: 220px;"
          />
          <q-input v-model="currentBook.publish_date" label="Publication Date" type="date" outlined />
          <q-input v-model="currentBook.isbn" label="ISBN" outlined />
        </q-card-section>

        <q-card-actions>
          <q-btn color="primary" @click="updateBook">Update</q-btn>
          <q-btn @click="editBookDialog = false">Close</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Add Author Dialog -->
    <q-dialog v-model="addAuthorDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Add New Author</div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="newAuthor.first_name" label="Author First Name" outlined />
          <q-input v-model="newAuthor.last_name" label="Author Last Name" outlined />
          <q-input v-model="newAuthor.date_of_birth" label="Author Date of Birth" type="date" outlined />
        </q-card-section>

        <q-card-actions>
          <q-btn color="primary" @click="addAuthor">Add</q-btn>
          <q-btn @click="addAuthorDialog = false">Close</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Edit Author Dialog -->
    <q-dialog v-model="editAuthorDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Edit Author</div>
        </q-card-section>

        <q-card-section>
          <q-input v-model="currentAuthor.first_name" label="Author First Name" outlined />
          <q-input v-model="currentAuthor.last_name" label="Author Last Name" outlined />
          <q-input v-model="currentAuthor.date_of_birth" label="Author Date of Birth" type="date" outlined />
        </q-card-section>

        <q-card-actions>
          <q-btn color="primary" @click="updateAuthor">Update</q-btn>
          <q-btn @click="editAuthorDialog = false">Close</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>




<script>
import { Notify } from 'quasar';

export default {
  data() {
    return {
      books: [],
      authors: [],
      authorsOptions: [],
      bookColumns: [
        { name: 'title', label: 'Title', align: 'left', field: row => row.title },
        {
          name: 'authors',
          label: 'Author(s)',
          align: 'left',
          field: row => this.getAuthors(row.authors)
        },
        { name: 'publish_date', label: 'Publication Date', align: 'left', field: row => row.publish_date },
        { name: 'isbn', label: 'ISBN', align: 'left', field: row => row.isbn },
        { name: 'edit', label: '', align: 'center' },
        { name: 'delete', label: '', align: 'center' }
      ],
      authorColumns: [
        { name: 'first_name', label: 'First Name', align: 'left', field: row => row.first_name },
        { name: 'last_name', label: 'Last Name', align: 'left', field: row => row.last_name },
        { name: 'date_of_birth', label: 'Date of Birth', align: 'left', field: row => row.date_of_birth },
        { name: 'edit', label: '', align: 'center' },
        { name: 'delete', label: '', align: 'center' }
      ],
      paginationBooks: {
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 0
      },
      paginationAuthors: {
        page: 1,
        rowsPerPage: 10,
        rowsNumber: 0
      },
      addBookDialog: false,
      editBookDialog: false,
      addAuthorDialog: false,
      editAuthorDialog: false,
      newBook: {
        title: '',
        authors: [],
        publish_date: '',
        isbn: ''
      },
      currentBook: {},
      newAuthor: {
        first_name: '',
        last_name: '',
        date_of_birth: ''
      },
      currentAuthor: {}
    };
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await this.$axios.get('/api/books/', {
          params: {
            page: this.paginationBooks.page,
            page_size: this.paginationBooks.rowsPerPage,
          }
        });
        this.books = response.data.results;
        this.paginationBooks.rowsNumber = response.data.count;
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error loading books!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    async fetchAuthors() {
      try {
        const response = await this.$axios.get('/api/authors/',
          {
            params: {
              page: this.paginationAuthors.page,
              page_size: this.paginationAuthors.rowsPerPage,
            }
          }
        );
        this.authors = response.data.results;
        this.paginationAuthors.rowsNumber = response.data.count;
        this.authorsOptions = this.authors.map(author => ({
          label: `${author.first_name} ${author.last_name} (${author.date_of_birth})`,
          name: `${author.first_name} ${author.last_name}`,
          value: author.id
        }));
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error loading authors!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    changeBookPage(page) {
      this.paginationBooks.page = page;
      this.fetchBooks();
    },
    changeAuthorPage(page) {
      this.paginationAuthors.page = page;
      this.fetchAuthors();
    },
    openAddBookDialog() {
      this.newBook = {
        title: '',
        authors: [],
        publish_date: '',
        isbn: ''
      };
      this.addBookDialog = true;
    },
    async addBook() {
      try {
        const token = localStorage.getItem('token');
        await this.$axios.post('/api/books/', this.newBook, {
          headers: {
            Authorization: `Token ${token}`
          }});
        this.addBookDialog = false;
        this.fetchBooks();
        Notify.create({ type: 'positive', message: 'Book added successfully' });
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error adding a book!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    editBook(book) {
      this.currentBook = { ...book };
      this.editBookDialog = true;
    },
    async updateBook() {
      try {
        const token = localStorage.getItem('token');
        await this.$axios.put(`/api/books/${this.currentBook.id}/`, this.currentBook, {
          headers: {
            Authorization: `Token ${token}`
          }});
        this.editBookDialog = false;
        this.fetchBooks();
        Notify.create({ type: 'positive', message: 'Book updated successfully' });
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error updating book!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    async deleteBook(bookId) {
      try {
        const token = localStorage.getItem('token');
        await this.$axios.delete(`/api/books/${bookId}/`, {
          headers: {
            Authorization: `Token ${token}`
          }});
        this.fetchBooks();
        Notify.create({ type: 'positive', message: 'Book deleted successfully' });
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error deleting book!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    openAddAuthorDialog() {
      this.newAuthor = {
        first_name: '',
        last_name: '',
        date_of_birth: ''
      };
      this.addAuthorDialog = true;
    },
    async addAuthor() {
      try {
        const token = localStorage.getItem('token');
        await this.$axios.post('/api/authors/', this.newAuthor, {
          headers: {
            Authorization: `Token ${token}`
          }});
        this.addAuthorDialog = false;
        this.fetchAuthors();
        Notify.create({ type: 'positive', message: 'Author added successfully' });
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error adding an author!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    editAuthor(author) {
      this.currentAuthor = { ...author };
      this.editAuthorDialog = true;
    },
    async updateAuthor() {
      try {
        const token = localStorage.getItem('token');
        await this.$axios.put(`/api/authors/${this.currentAuthor.id}/`, this.currentAuthor, {
          headers: {
            Authorization: `Token ${token}`
          }});
        this.editAuthorDialog = false;
        this.fetchAuthors();
        Notify.create({ type: 'positive', message: 'Author updated successfully' });
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error updating and author!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    async deleteAuthor(authorId) {
      try {
        const token = localStorage.getItem('token');
        await this.$axios.delete(`/api/authors/${authorId}/`, {
          headers: {
            Authorization: `Token ${token}`
          }});
        this.fetchAuthors();
        Notify.create({ type: 'positive', message: 'Author deleted successfully' });
      } catch (error) {
        if(error.response)
        {
          const errorData = error.response.data['errors'];
          let errorMessages;
          if(errorData){
            errorMessages = Object.entries(errorData)
              .map(([field, messages]) => 
                `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`
              )
              .join(' ');
          }
          else
          {
            errorMessages = error.response.data['error'] ? error.response.data['error'] : 'You have to log in to do it.';
          }
          Notify.create({
            message: 'Error deleting an author!' +  (` ${errorMessages}`),
            color: 'negative',
            position: 'top'
          });         
        }
      }
    },
    getAuthors(authorIDs) { //this has to be synchronous because the authors cannot be received from the fetched ones as some of them may be on the other page and thus wont be present in fetched which will result in blanks in table.
      let out = '';
      for (const element of authorIDs) {
        const name = this.getAuthorName(element);
        out += name;
        out += ', ';
      }
      return out;
    },

    getAuthorName(authorId) {
      try {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", `/api/authors/${authorId}/`, false);
        xhr.send(null);

        if (xhr.status === 200) {
          const response = JSON.parse(xhr.responseText);
          return `${response['first_name']} ${response['last_name']}`;
        } else {
          return '';
        }
      } catch {
        return '';
      }
    }
  },
  watch: {
    'paginationBooks.rowsPerPage'(newRowsPerPage) {
      this.paginationBooks.page=1;
      this.fetchBooks();
    },
    'paginationAuthors.rowsPerPage'(newRowsPerPage) {
      this.paginationAuthors.page=1;
      this.fetchAuthors();
    }
  },
  created() {
    this.fetchAuthors();
    this.fetchBooks();
  }
};
</script>


<style scoped>
.q-page {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
