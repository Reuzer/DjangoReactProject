import styles from './Register.module.css';
import { useState } from 'react';
import { RegisterUser } from '../../api/types';
import { authStore } from '../../stores/AuthStore';
import { useNavigate } from 'react-router';

const Register = () => {

    const navigate = useNavigate();
    const [formData, setFormData] = useState<RegisterUser>({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        middle_name: '',
        phone: '',
      });
    
      const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
      };
    
      const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await authStore.register(formData);
        navigate('/')
        location.reload();
      };
    
      return (
        <form onSubmit={handleSubmit} className={styles.form}>
          <h1>Регистрация</h1>
          {authStore.error && <div style={{ color: 'red' }}>{authStore.error}</div>}
          <div className={styles.form_wrapper}>
            <label htmlFor={'username'}>
              Имя пользователя:
              </label><br/>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            
          </div>
          <div>
            <label htmlFor='email'>
              Email:
              </label><br />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            
          </div>
          <div>
            <label>
              Пароль:<br />
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Имя:<br />
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Фамилия:<br />
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
              />
            </label>
          </div>
          <div>
            <label>
              Отчество:<br />
              <input
                type="text"
                name="middle_name"
                value={formData.middle_name}
                onChange={handleChange}
              />
            </label>
          </div>
          <div>
            <label>
              Телефон:<br />
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
              />
            </label>
          </div>
          <button type="submit" disabled={authStore.isLoading}>
            {authStore.isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
          </button>
        </form>
      );
}
 
export default Register;