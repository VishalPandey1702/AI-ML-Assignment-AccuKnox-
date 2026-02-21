import streamlit as st
import pandas as pd

from services.book_service import BookService
from services.student_service import StudentService
from services.user_service import UserService
from database.db import initialize_database

st.set_page_config(
    page_title="AI-ML Assignment",
    page_icon="📚",
    layout="wide"
)

@st.cache_resource
def get_services():
    initialize_database()
    return {
        'books': BookService(),
        'students': StudentService(),
        'users': UserService()
    }

def render_sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")
    
    option = st.sidebar.radio(
        "Select Module",
        ["📚 Books API", "📊 Student Scores", "👥 CSV Import"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "This app demonstrates:\n"
        "- REST API integration\n"
        "- SQLite database\n"
        "- Data visualization\n"
        "- CSV file processing"
    )
    
    return option

def render_books_module(book_service):
    st.header("📚 Books API Module")
    st.write("Fetch books from Open Library API and store in SQLite database")
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("Search Query", value="python programming")
    
    with col2:
        limit = st.number_input("Max Results", min_value=1, max_value=50, value=10)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fetch_btn = st.button("🔄 Fetch Books", type="primary", use_container_width=True)
    
    with col2:
        refresh_btn = st.button("📖 Show Stored Books", use_container_width=True)
    
    with col3:
        clear_btn = st.button("🗑️ Clear Database", use_container_width=True)
    
    st.markdown("---")
    
    if fetch_btn:
        with st.spinner(f"Fetching books for '{search_query}'..."):
            try:
                result = book_service.fetch_and_store_books(search_query, limit)
                
                if result['success']:
                    st.success(f"Fetched {result['fetched']} books and saved {result['saved']} to database!")
                else:
                    st.error(f"Error: {result['error']}")
            except Exception as e:
                st.error(f"Failed to fetch books: {e}")
    
    if clear_btn:
        deleted = book_service.clear_books()
        st.info(f"Cleared {deleted} books from database")
    
    st.subheader("Stored Books")
    
    books = book_service.get_books_from_db()
    
    if books:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", len(books))
        with col2:
            authors = len(set(b['author'] for b in books))
            st.metric("Unique Authors", authors)
        with col3:
            years = [b['publication_year'] for b in books if b['publication_year']]
            avg_year = int(sum(years) / len(years)) if years else 'N/A'
            st.metric("Avg. Publication Year", avg_year)
        
        df = pd.DataFrame(books)
        df = df[['title', 'author', 'publication_year', 'isbn']]
        df.columns = ['Title', 'Author', 'Year', 'ISBN']
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No books in database. Click 'Fetch Books' to get started!")

def render_student_module(student_service):
    st.header("📊 Student Scores Module")
    st.write("Fetch student test scores, calculate statistics, and visualize with charts")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fetch_btn = st.button("🔄 Generate Scores", type="primary", use_container_width=True)
    
    with col2:
        refresh_btn = st.button("📊 Refresh Data", use_container_width=True)
    
    with col3:
        clear_btn = st.button("🗑️ Clear Data", use_container_width=True)
    
    st.markdown("---")
    
    if fetch_btn:
        with st.spinner("Generating student score data..."):
            result = student_service.fetch_and_store_data()
            
            if result['success']:
                st.success(
                    f"Generated {result['fetched']} records, "
                    f"saved {result['saved']} to database. "
                    f"Average score: {result['average_score']}"
                )
            else:
                st.error(f"Error: {result['error']}")
    
    if clear_btn:
        deleted = student_service.clear_students()
        st.info(f"Cleared {deleted} student records")
    
    students = student_service.get_student_data()
    
    if not students:
        st.info("No student data. Click 'Generate Scores' to create sample data!")
        return
    
    stats = student_service.calculate_statistics()
    
    st.subheader("Statistics Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Score", f"{stats['average_score']}%")
    with col2:
        st.metric("Total Records", stats['total_records'])
    with col3:
        st.metric("Unique Students", stats['unique_students'])
    with col4:
        st.metric("Subjects", stats['unique_subjects'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Highest Score", f"{stats['max_score']}%")
    with col2:
        st.metric("Lowest Score", f"{stats['min_score']}%")
    
    st.markdown("---")
    
    st.subheader("Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Average Score by Subject**")
        subject_scores = student_service.get_scores_by_subject()
        if subject_scores:
            df_subjects = pd.DataFrame({
                'Subject': list(subject_scores.keys()),
                'Average Score': list(subject_scores.values())
            })
            st.bar_chart(df_subjects.set_index('Subject'))
    
    with col2:
        st.write("**Top Performers**")
        top_performers = student_service.get_top_performers(5)
        if top_performers:
            df_top = pd.DataFrame(top_performers)
            df_top.columns = ['Student', 'Avg Score', 'Subjects']
            st.bar_chart(df_top.set_index('Student')['Avg Score'])
    
    st.markdown("---")
    
    st.subheader("Scores by Student")
    student_scores = student_service.get_scores_by_student()
    if student_scores:
        df_students = pd.DataFrame({
            'Student': list(student_scores.keys()),
            'Average Score': list(student_scores.values())
        })
        st.dataframe(df_students, use_container_width=True, hide_index=True)
    
    with st.expander("View All Records"):
        df = pd.DataFrame(students)
        df = df[['name', 'subject', 'score']]
        df.columns = ['Name', 'Subject', 'Score']
        st.dataframe(df, use_container_width=True, hide_index=True)

def render_csv_module(user_service):
    st.header("👥 CSV Import Module")
    st.write("Upload a CSV file with user information and import into SQLite database")
    
    st.markdown("---")
    
    with st.expander("CSV Format Requirements"):
        st.markdown("""
        Your CSV file should have the following columns:
        - **name** (required): User's full name
        - **email** (required): User's email address
        - **phone** (optional): User's phone number
        
        Example:
        ```
        name,email,phone
        John Doe,john@example.com,555-1234
        Jane Smith,jane@example.com,555-5678
        ```
        """)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        import_btn = st.button("📥 Import Users", type="primary", use_container_width=True, 
                               disabled=(uploaded_file is None))
    
    with col2:
        clear_btn = st.button("🗑️ Clear All Users", use_container_width=True)
    
    st.markdown("---")
    
    if uploaded_file is not None and import_btn:
        with st.spinner("Importing users..."):
            file_content = uploaded_file.getvalue()
            result = user_service.import_from_upload(file_content, uploaded_file.name)
            
            if result['success']:
                st.success(
                    f"Import complete! "
                    f"Imported: {result['imported']}, "
                    f"Skipped: {result['skipped']}"
                )
                
                if result['errors']:
                    with st.expander("Import Warnings"):
                        for error in result['errors']:
                            st.warning(error)
            else:
                st.error(f"Import failed: {result['error']}")
    
    if clear_btn:
        deleted = user_service.clear_users()
        st.info(f"Cleared {deleted} users from database")
    
    st.subheader("Stored Users")
    
    users = user_service.get_all_users()
    
    if users:
        stats = user_service.get_statistics()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", stats['total_users'])
        with col2:
            st.metric("With Phone", stats['with_phone'])
        with col3:
            st.metric("Without Phone", stats['without_phone'])
        
        search_term = st.text_input("Search users by name or email")
        
        if search_term:
            users = user_service.search_users(search_term)
            st.info(f"Found {len(users)} matching users")
        
        if users:
            df = pd.DataFrame(users)
            df = df[['name', 'email', 'phone', 'created_at']]
            df.columns = ['Name', 'Email', 'Phone', 'Created At']
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No users in database. Upload a CSV file to get started!")
    
    st.markdown("---")
    st.subheader("Download Sample CSV")
    
    sample_csv = """name,email,phone
John Doe,john.doe@example.com,555-0101
Jane Smith,jane.smith@example.com,555-0102
Bob Johnson,bob.johnson@example.com,555-0103
Alice Williams,alice.williams@example.com,555-0104
Charlie Brown,charlie.brown@example.com,555-0105"""
    
    st.download_button(
        label="Download Sample CSV",
        data=sample_csv,
        file_name="sample_users.csv",
        mime="text/csv"
    )

def main():
    services = get_services()
    
    selected_module = render_sidebar()
    
    if "Books API" in selected_module:
        render_books_module(services['books'])
    
    elif "Student Scores" in selected_module:
        render_student_module(services['students'])
    
    elif "CSV Import" in selected_module:
        render_csv_module(services['users'])
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888;'>"
        "AI-ML Assignment | Python, Streamlit & SQLite"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
