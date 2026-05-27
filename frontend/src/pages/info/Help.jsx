import { Link } from 'react-router-dom';
import InfoPage from '../../components/layout/InfoPage';

export default function Help() {
  return (
    <InfoPage title="Помощь">
      <p>
        <strong>Как зарегистироваться?</strong> Создайте аккаунт на странице{' '}
        <Link to="/register" className="font-medium underline">
          регистрации
        </Link>
        .
      </p>
      <p>
        <strong>Как опубликовать?</strong> После входа нажмите «Опубликовать», загрузите изображение,
        укажите категорию и описание.
      </p>
      <p>
        <strong>Как изменить профиль?</strong> В личном кабинете можно изменить аватар, биографию и
        интересы.
      </p>
      <p>
        <strong>Проблемы с доступом?</strong> Если аккаунт заблокирован, обратитесь к
        администратору платформы.
      </p>
    </InfoPage>
  );
}
