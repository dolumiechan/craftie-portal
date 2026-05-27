/**
 * Извлекает читаемое сообщение об ошибке из ответа FastAPI / axios.
 */
export function getApiErrorMessage(error, fallback = 'Произошла ошибка. Попробуйте ещё раз.') {
  if (!error) return fallback;

  const detail = error.response?.data?.detail;

  if (typeof detail === 'string') return detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => item.msg || item.message || JSON.stringify(item))
      .join('. ');
  }

  if (error.message === 'Network Error') {
    return 'Нет связи с сервером. Проверьте, что бэкенд запущен.';
  }

  if (error.response?.status === 403) {
    return 'Недостаточно прав для этого действия.';
  }

  if (error.response?.status === 404) {
    return 'Запрашиваемые данные не найдены.';
  }

  return fallback;
}
